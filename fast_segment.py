import os
import argparse
from concurrent.futures import ThreadPoolExecutor


def segment(input_dir):
    futures = []
    with ThreadPoolExecutor(32) as pool:
        for root, dirs, files in os.walk(input_dir):
            def task(root, files):
                for file in files:
                    if 'T1' in file:
                        os.system(
                            f"fast --class=3 --out={os.path.join(root, file)} {os.path.join(root, file)}")
            futures += [pool.submit(task, root, files)]
    for future in futures:
        future.result()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Registration')
    parser.add_argument('-i', '--input_dir', type=str, help='input directory')
    args = parser.parse_args()
    segment(args.input_dir)
