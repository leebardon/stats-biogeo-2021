import pandas as pd
import pickle

NO3, PO4, SI, FE = "TRAC04", "TRAC05", "TRAC06", "TRAC07"


def get_data(path, *filenames):
    data = []
    for name in filenames:
        data.append(pd.read_pickle(f"{path}/{name}"))
    return [data[i] for i in range(len(data))]


def return_predictor_dataset(ecosys, sss, sst, par):
    nutrients = ecosys[["Month", "X", "Y", PO4, NO3, FE, SI]]
    predictor_dataset = add_predictor(nutrients, sst)
    predictor_dataset = add_predictor(predictor_dataset, sss)
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


def group_plankton(eco, eco_r, eco_f, eco_rf, *nums):
    group = ["TRAC" + str(num) for num in nums]
    return (
        sum([eco[g] for g in group]),
        sum([eco_r[g] for g in group]),
        sum([eco_f[g] for g in group]),
        sum([eco_rf[g] for g in group]),
    )


def group_oce_plank(eco_oce, eco_oce_f, *nums):
    group = ["TRAC" + str(num) for num in nums]
    return (
        sum([eco_oce[g] for g in group]),
        sum([eco_oce_f[g] for g in group]),
    )


def get_arr(type):
    plank = [prok, pico, cocco, diazo, diatom, dino, zoo]
    return
    if type == 1:
        return [f"{p}" for p in plank]
    elif type == 2:
        return [f"{p}_r" for p in plank]
    elif type == 3:
        return [f"{p}_val" for p in plank]
    else:
        return [f"{p}_val_f" for p in plank]
