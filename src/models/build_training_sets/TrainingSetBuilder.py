import pandas as pd
import pickle

NO3, PO4, Si, Fe = "TRAC04", "TRAC05", "TRAC06", "TRAC07"


def return_predictor_dataset(ecosys, sss, sst, par):
    nutrients = ecosys[["Month", "X", "Y", NO3, PO4, Si, Fe]]
    predictor_dataset = add_predictor(nutrients, sss)
    predictor_dataset = add_predictor(predictor_dataset, sst)
    predictor_dataset = add_predictor(predictor_dataset, par)
    predictor_dataset.rename(
        {"TRAC04": "NO3", "TRAC05": "PO4", "TRAC06": "Si", "TRAC07": "Fe"},
        axis=1,
        inplace=True,
    )
    predictor_dataset.drop(["Month", "X", "Y"], axis=1, inplace=True)
    return predictor_dataset


def add_predictor(predictor_df, new_predictor):
    return predictor_df.merge(
        new_predictor,
        left_on=["Month", "X", "Y"],
        right_on=["Month", "X", "Y"],
        how="inner",
    )


def group_plankton(ecosys, *nums):
    group_members = ["TRAC" + str(num) for num in nums]
    group_summed = sum([ecosys[member] for member in group_members])
    return group_summed


def save_plankton_sets(save_path, plankton_arr, set_type):
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
