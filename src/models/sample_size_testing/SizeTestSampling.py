import numpy as np
import pandas as pd


def reshape_test_matrices(*matrices):
    reshaped = []
    for M in matrices[0]:
        pos_M = np.where(M == 1)
        reshaped_M = np.vstack((pos_M[0], pos_M[1], pos_M[2])).T
        reshaped.append(reshaped_M)
    return reshaped


def return_test_dataframes(*matrices):
    dfs = []
    for M in matrices[0]:
        M_df = pd.DataFrame((M[:, 0], M[:, 1], M[:, 2])).T
        M_df.columns = ["X", "Y", "Month"]
        dfs.append(M_df)
    return dfs


def merge_test_matrices_and_ecosys_data(matrices, ecosys_data):
    merged_dfs = []
    for M in matrices:
        merged = ecosys_data.merge(M, on=["X", "Y", "Month"], how="inner")
        merged_dfs.append(merged)
    return merged_dfs


def check_land_removed(matrices):
    land_removed = []
    for M_df in matrices:
        ocean = M_df[M_df["pCO2"] != 0]
        land_removed.append(ocean)
    return land_removed
