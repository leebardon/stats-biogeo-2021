import os
import pickle
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


def plankton_sets(save_path, plankton_arr, set_type):
    plankton = {
        "proko": plankton_arr[0],
        "pico": plankton_arr[1],
        "cocco": plankton_arr[2],
        "diazo": plankton_arr[3],
        "diatom": plankton_arr[4],
        "dino": plankton_arr[5],
        "zoo": plankton_arr[6],
    }
    with open(f"{save_path}/plankton_{set_type}.pkl", "wb") as handle:
        pickle.dump(plankton, handle, protocol=pickle.HIGHEST_PROTOCOL)
