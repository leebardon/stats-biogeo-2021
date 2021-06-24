import numpy as np
import pandas as pd


def get_matrices(path, *matrices):
    mats = []
    for matrix in matrices:
        mats.append(np.load(f"{path}/{matrix}.npy"))
    return [m for m in mats]


def reshape_matrices(*matrices):
    mats = []
    for matrix in matrices:
        pos_I = np.where(matrix == 1)
        mats.append(np.vstack((pos_I[0], pos_I[1], pos_I[2])).T)
    return [m for m in mats]


def return_dataframes(*matrices):
    mats = []
    for matrix in matrices:
        I_df = pd.DataFrame((matrix[:, 0], matrix[:, 1], matrix[:, 2])).T
        I_df.columns = ["X", "Y", "Month"]
        mats.append(I_df)
    return [m for m in mats]

def get_ecosys_data(path, *files):
    data = []
    for file in files:
        data.append(pd.read_pickle(f"{path}/{file}.pkl"))
    return [d for d in data]


def merge_matrix_and_ecosys_data(sampling_matrix, ecosys_data):
    merged_df = ecosys_data.merge(sampling_matrix, on=["X", "Y", "Month"], how="inner")
    return merged_df


def remove_land(df):
    land_removed = df[df["pCO2"] != 0]
    return land_removed


def make_equal(sampled_set, randomly_sampled_set):
    randomly_sampled_set.drop(
        randomly_sampled_set.tail(
            (randomly_sampled_set.shape[0] - sampled_set.shape[0])
        ).index,
        inplace=True,
    )
    return randomly_sampled_set
