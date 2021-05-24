import os
import pickle
import numpy as np

# ADD SOMETHING TO SAVE OUTPUT FILE DETAILING E.G. SHAPE, MIN AND MAX X/Y


def check_dir_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def save_to_pkl(path, **kwargs):
    check_dir_exists(path)
    for filename, df in kwargs.items():
        df.to_pickle(f"{path}/{filename}")


def save_matrix(path, **matrices):
    check_dir_exists(path)
    for filename, matrix in matrices.items():
        np.save(
            f"{path}/{filename}",
            matrix,
            allow_pickle=True,
        )


def plankton_dicts(path, **dictionary_sets):
    for filename, arr in dictionary_sets.items():
        plankton = {
            "Pro": arr[0],
            "Pico": arr[1],
            "Cocco": arr[2],
            "Diazo": arr[3],
            "Diatom": arr[4],
            "Dino": arr[5],
            "Zoo": arr[6],
        }
        with open(f"{path}/{filename}.pkl", "wb") as handle:
            pickle.dump(plankton, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save_gams(path, **gams_sets):
    for group, gam in gams_sets.items():
        with open(f"{path}/{group}.pkl", "wb") as handle:
            pickle.dump(gam, handle, protocol=pickle.HIGHEST_PROTOCOL)
