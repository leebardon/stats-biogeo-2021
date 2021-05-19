import os
import pickle
import numpy as np

# ADD SOMETHING TO SAVE OUTPUT FILE DETAILING E.G. SHAPE, MIN AND MAX X/Y


def check_dir_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


def save_to_pkl(path, **kwargs):
    check_dir_exists(path)
    for filename, df in kwargs.items():
        df.to_pickle(f"{path}/{filename}")


def save_matrix(path, **kwargs):
    check_dir_exists(path)
    for filename, matrix in kwargs.items():
        np.save(
            f"{path}/{filename}",
            matrix,
            allow_pickle=True,
        )


def plankton_sets(save_path, plankton_arr, set_type):
    plankton = {
        "pro": plankton_arr[0],
        "pico": plankton_arr[1],
        "cocco": plankton_arr[2],
        "diazo": plankton_arr[3],
        "diatom": plankton_arr[4],
        "dino": plankton_arr[5],
        "zoo": plankton_arr[6],
    }
    with open(f"{save_path}/plankton_{set_type}.pkl", "wb") as handle:
        pickle.dump(plankton, handle, protocol=pickle.HIGHEST_PROTOCOL)
