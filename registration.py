import os
import argparse
from concurrent.futures import ThreadPoolExecutor


def register(input_dir, output_dir, ref_path):
    with ThreadPoolExecutor(8) as pool:
        for root, dirs, files in os.walk(input_dir):
            def task(root, files):
                out_path = root.replace(input_dir, output_dir)
                os.makedirs(out_path, exist_ok=True)
                for file in files:
                    if os.path.exists(os.path.join(out_path, file)):
                        continue
                    if (file.endswith(".nii.gz") or file.endswith(".nii")) and 'seg' not in file:
                        os.system(
                            f"flirt -in {os.path.join(root, file)} -ref {ref_path} -out {os.path.join(out_path, file)} \
                                -omat /tmp/{os.path.basename(root)}-affine.mat")
                for file in files:
                    if os.path.exists(os.path.join(out_path, file)):
                        continue
                    if 'seg' in file:
                        os.system(
                            f"flirt -in {os.path.join(root, file)} -ref {ref_path} -out {os.path.join(out_path, file)} \
                                -applyxfm -init /tmp/{os.path.basename(root)}-affine.mat"
                        )
            pool.submit(task, root, files)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Registration')
    parser.add_argument('-i', '--input_dir', type=str, help='input directory')
    parser.add_argument('-o', '--output_dir', type=str,
                        help='output directory')
    parser.add_argument('-r', '--ref_path', type=str, help='reference image')
    args = parser.parse_args()
    register(args.input_dir, args.output_dir, args.ref_path)
