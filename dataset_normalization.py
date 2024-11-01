import os
import argparse


def normalize_dataset(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".nii.gz") or file.endswith(".nii"):
                basename = os.path.basename(file).split('.')[0]
                name_parts = basename.split("-")
                label = name_parts[0]
                if not os.path.exists(os.path.join(output_dir, label)):
                    os.makedirs(os.path.join(output_dir, label))
                os.system(
                    f"cp {os.path.join(root, file)} {os.path.join(output_dir, label)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_dir", type=str,
                        default="data", help="input directory")
    parser.add_argument("-o", "--output_dir", type=str,
                        default="data_normalized", help="output directory")
    args = parser.parse_args()

    normalize_dataset(args.input_dir, args.output_dir)
