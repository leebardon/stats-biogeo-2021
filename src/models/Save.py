import os
import numpy as np


def check_dir_exists(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            print(f"Creation of the directory {path} failed")
        else:
            continue


def save_to_pkl(df, path, filename):
    check_dir_exists(path)
    df.to_pickle(f"{path}/{filename}")


def save_matrix(matrix, path, filename):
    check_dir_exists(path)
    np.save(
        f"{path}/{filename}",
        matrix,
        allow_pickle=True,
    )
