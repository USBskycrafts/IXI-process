import os
import argparse
from tqdm import tqdm


def reoreint_images(input_dir, output_dir):
    pbar = os.walk(input_dir)
    for root, _, files in pbar:
        for file in files:
            if file.endswith('.nii.gz') or file.endswith('.nii'):
                out_path = root.replace(input_dir, output_dir)
                os.makedirs(out_path, exist_ok=True)
                os.system(
                    f'fslreorient2std {os.path.join(root, file)} {os.path.join(out_path, file)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reorient a set of images.')
    parser.add_argument('-i', '--input_dir', type=str,
                        help='Input directory containing images.')
    parser.add_argument('-o', '--output_dir', type=str,
                        help='Output directory to save reoriented images.')
    args = parser.parse_args()
    reoreint_images(args.input_dir, args.output_dir)
