
import os
import argparse
from tqdm import tqdm
from multiprocessing import Process
from pathlib import Path


def reoreint_images(input_dir, output_dir):
    pbar = os.walk(input_dir)
    for root, _, files in pbar:
        for file in files:
            if file.endswith('.nii.gz') or file.endswith('.nii'):
                out_path = root.replace(input_dir, output_dir)
                os.makedirs(out_path, exist_ok=True)
                os.system(
                    f'mri_synthstrip -i {os.path.join(root, file)} -o {os.path.join(out_path, file)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reorient a set of images.')
    parser.add_argument('-i', '--input_dir', type=Path,
                        help='Input directory containing images.')
    parser.add_argument('-o', '--output_dir', type=Path,
                        help='Output directory to save reoriented images.')
    args = parser.parse_args()
    reoreint_images(str(args.input_dir), str(args.output_dir))
