import os
import argparse
import random


def split_dataset(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        dir_name = os.path.basename(root)
        if all(file.endswith(".nii.gz") or file.endswith(".nii") for file in files):
            if len(files) < 3:
                print(
                    f"Skipping {root} because it does not contain enough files")
                continue
            if not os.path.exists(os.path.join(output_dir, 'train')):
                os.makedirs(os.path.join(output_dir, 'train'))
            if not os.path.exists(os.path.join(output_dir, 'val')):
                os.makedirs(os.path.join(output_dir, 'val'))
            if not os.path.exists(os.path.join(output_dir, 'test')):
                os.makedirs(os.path.join(output_dir, 'test'))
            num = random.randrange(0, 100)
            if num < 80:
                os.system(
                    f"cp -r {root} {os.path.join(output_dir, 'train')}")
            elif num < 90:
                os.system(
                    f"cp -r {root} {os.path.join(output_dir, 'val')}")
            else:
                os.system(
                    f"cp -r {root} {os.path.join(output_dir, 'test')}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", type=str,
                        default="data", help="input directory")
    parser.add_argument("-o", "--output_dir", type=str,
                        default="data_normalized", help="output directory")
    args = parser.parse_args()

    split_dataset(args.input_dir, args.output_dir)
