import os
import argparse
from multiprocessing import Process
from multiprocessing.pool import ThreadPool


def register(input_dir, output_dir, ref_path):
    with ThreadPool(64) as pool:
        for root, dirs, files in os.walk(input_dir):
            def task(root, files):
                out_path = root.replace(input_dir, output_dir)
                os.makedirs(out_path, exist_ok=True)
                for file in files:
                    if os.path.exists(os.path.join(out_path, file)):
                        continue
                    if (file.endswith(".nii.gz") or file.endswith(".nii")) and 'seg' not in file:
                        os.system(
                            f"fnirt --in={os.path.join(root, file)} --ref={ref_path} --iout={os.path.join(out_path, file)} \
                                --fout=/tmp/{os.path.basename(root)}-affine.mat")
                for file in files:
                    if os.path.exists(os.path.join(out_path, file)):
                        continue
                    if 'seg' in file:
                        os.system(
                            f"applywarp --in={os.path.join(root, file)} --ref={ref_path} --out={os.path.join(out_path, file)} \
                                --premat=/tmp/{os.path.basename(root)}-affine.mat"
                        )
            pool.apply_async(task, (root, files))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Registration')
    parser.add_argument('-i', '--input_dir', type=str, help='input directory')
    parser.add_argument('-o', '--output_dir', type=str,
                        help='output directory')
    parser.add_argument('-r', '--ref_path', type=str, help='reference image')
    args = parser.parse_args()
    register(args.input_dir, args.output_dir, args.ref_path)
