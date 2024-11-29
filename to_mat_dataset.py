import os
import argparse
import nibabel as nib
import numpy as np
from skimage.transform import resize
import h5py


def transform2png(input_dir, output_dir):
    records = {}
    for root, dirs, files in os.walk(input_dir):
        if not any(f.endswith('.nii.gz') for f in files):
            continue
        for file in files:
            if 'T2' in file:
                ndarray = nib.nifti1.load(
                    os.path.join(root, file)
                ).get_fdata(dtype=np.float32)
                ndarray = np.pad(ndarray, ((18, 18), (0, 0), (0, 0)),
                                 mode='constant', constant_values='0')
                ndarray = resize(ndarray, (256, 256), mode='constant',
                                 anti_aliasing=False)
                ndarray -= ndarray.min()
                ndarray = (ndarray / np.percentile(ndarray, 99.9)).clip(0, 1)
                if not records.get('T2'):
                    records['T2'] = []

                ndarrays = np.array_split(
                    ndarray, ndarray.shape[2] // 3, axis=2)
                ndarrays = [
                    ndarray for ndarray in ndarrays if ndarray.shape[2] == 3]
                records['T2'].extend(ndarrays)
            elif 'PD' in file:
                ndarray = nib.nifti1.load(
                    os.path.join(root, file)
                ).get_fdata(dtype=np.float32)
                ndarray = np.pad(ndarray, ((18, 18), (0, 0), (0, 0)),
                                 mode='constant', constant_values='0')
                ndarray = resize(ndarray, (256, 256), mode='constant',
                                 anti_aliasing=False)
                ndarray -= ndarray.min()
                ndarray = (ndarray / np.percentile(ndarray, 99.9)).clip(0, 1)
                if not records.get('PD'):
                    records['PD'] = []

                ndarrays = np.array_split(
                    ndarray, ndarray.shape[2] // 3, axis=2)
                ndarrays = [
                    ndarray for ndarray in ndarrays if ndarray.shape[2] == 3]
                records['PD'].extend(ndarrays)
            else:
                continue
    assert len(records['T2']) == len(records['PD'])
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file = h5py.File(os.path.join(output_dir, 'data.mat'), 'w')

    data_x = np.stack(records['T2'], axis=0)
    data_x = data_x.transpose((2, 1, 0, 3))
    file.create_dataset('data_x', data=data_x)

    data_y = np.stack(records['PD'], axis=0)
    data_y = data_y.transpose((2, 1, 0, 3))
    file.create_dataset('data_y', data=data_y)

    print(data_x.shape, data_y.shape)
    file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, default='')
    parser.add_argument('--output_dir', type=str, default='')
    args = parser.parse_args()
    transform2png(args.input_dir, args.output_dir)
