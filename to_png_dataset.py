import os
import argparse
import nibabel as nib
import numpy as np
from PIL import Image
from skimage.transform import resize


def transform2png(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        if not any(f.endswith('.nii.gz') for f in files):
            continue
        record = {}
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
                record['T2'] = ndarray
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
                record['PD'] = ndarray
            else:
                continue
        record = np.concatenate((record['T2'], record['PD']), axis=1)
        record = np.split(record, record.shape[2], axis=2)
        for i, image in enumerate(record):
            image = Image.fromarray(
                (image * 255).astype(np.uint8).squeeze(), mode='L')
            save_path = root.replace(input_dir, output_dir)
            dir_name = os.path.dirname(save_path)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            # print(save_path)
            if os.path.exists(save_path + f'-{i}.png'):
                continue
            image.save(save_path + f'-{i}.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, default='')
    parser.add_argument('--output_dir', type=str, default='')
    args = parser.parse_args()
    transform2png(args.input_dir, args.output_dir)
