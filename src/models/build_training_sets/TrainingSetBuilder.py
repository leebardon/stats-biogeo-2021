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


def get_arr(type):
    plank = [prok, pico, cocco, diazo, diatom, dino, zoo]
    if type == 1:
        return plank
    elif type == 2:
        return [f"{p}_r" for p in plank]
    elif type == 3:
        return [f"{p}_val" for p in plank]
    else:
        return [f"{p}_val_f" for p in plank]
