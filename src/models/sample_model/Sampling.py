import numpy as np
import pandas as pd


def reshape_matrices(I, Ir):
    pos_I, pos_Ir = np.where(I == 1), np.where(Ir == 1)
    I = np.vstack((pos_I[0], pos_I[1], pos_I[2])).T
    Ir = np.vstack((pos_Ir[0], pos_Ir[1], pos_Ir[2])).T
    return I, Ir


def return_dataframes(I, Ir):
    I_df = pd.DataFrame((I[:, 0], I[:, 1], I[:, 2])).T
    Ir_df = pd.DataFrame((Ir[:, 0], Ir[:, 1], Ir[:, 2])).T
    I_df.columns, Ir_df.columns = ["X", "Y", "Month"], ["X", "Y", "Month"]
    return I_df, Ir_df


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
