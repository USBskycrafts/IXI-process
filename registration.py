import os
import argparse


def register(input_dir, output_dir, ref_path):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".nii.gz") or file.endswith(".nii"):
                out_path = root.replace(input_dir, output_dir)
                os.makedirs(out_path, exist_ok=True)
                os.system(
                    f"""flirt -in {os.path.join(root, file)} -ref {ref_path} -out {os.path.join(out_path, file)} -dof 12 -cost corratio""")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Registration')
    parser.add_argument('-i', '--input_dir', type=str, help='input directory')
    parser.add_argument('-o', '--output_dir', type=str,
                        help='output directory')
    parser.add_argument('-r', '--ref_path', type=str, help='reference image')
    args = parser.parse_args()
    register(args.input_dir, args.output_dir, args.ref_path)
