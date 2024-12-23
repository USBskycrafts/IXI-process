import numpy as np
from skimage.transform import resize
import argparse
import nibabel as nib
import os


def rank(tensor, num):
    tensor = np.sort(tensor.flatten())
    rank = np.where(tensor == num)[0][0] / len(tensor.flatten())
    return rank


def calculate_variance(data):
    pd, t1, t2 = data
    pd = pd / np.exp(-0.2)
    # print('min', np.min(pd - t1), np.min(pd - t2))
    # print('percentile of 0', rank(pd - t1, 0), rank(pd - t2, 0))
    return rank(pd - t1, 0), rank(pd - t2, 0)


def normalize(atlas):
    atlas = np.pad(atlas, ((18, 18), (0, 0), (0, 0)),
                   mode='constant', constant_values='0')
    atlas = resize(atlas, (256, 256), mode='constant',
                   anti_aliasing=False)
    atlas -= atlas.min()
    atlas = (atlas / np.percentile(atlas, 99.9)).clip(0, 1)

    # transform to torch.Tensor
    return atlas


def walk_dataset(work_dir):

    result = []

    for root, dirs, files in os.walk(work_dir):
        if not any(['nii' in file for file in files]):
            continue
        sample = [None for _ in range(3)]
        for file in files:
            if 'PD' in file:
                sample[0] = nib.nifti1.load(
                    os.path.join(root, file)).get_fdata()
            elif 'T1' in file:
                sample[1] = nib.nifti1.load(
                    os.path.join(root, file)).get_fdata()
            elif 'T2' in file:
                sample[2] = nib.nifti1.load(
                    os.path.join(root, file)).get_fdata()
            else:
                continue
        # sample = [normalize(sample[i]) for i in range(3)]
        # sample[1] = sample[1] * np.min((sample[0] + 1e-7) / (sample[1] + 1e-7))
        # sample[2] = sample[2] * np.min((sample[0] + 1e-7) / (sample[2] + 1e-7))
        result.append(calculate_variance(sample))
        print(np.mean(result, axis=0))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work_dir', type=str, default='')
    args = parser.parse_args()
    walk_dataset(args.work_dir)
