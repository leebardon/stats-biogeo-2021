import pandas as pd
import numpy as np
from pygam import LinearGAM

NO3, PO4, SI, FE = "TRAC04", "TRAC05", "TRAC06", "TRAC07"


def build_predictor_tsets(ecosys_dfs, sss, sst, par):
    predictors = []
    for df in ecosys_dfs:
        nutrients = df[["Month", "X", "Y", PO4, NO3, FE, SI]]
        adding_sst = add_predictor(nutrients, sst)
        adding_sss = add_predictor(adding_sst, sss)
        predictor_dataset = add_predictor(adding_sss, par)
        predictor_dataset.rename(
            {"TRAC04": "NO3", "TRAC05": "PO4", "TRAC06": "Si", "TRAC07": "Fe"},
            axis=1,
            inplace=True,
        )
        predictor_dataset.drop(["Month", "X", "Y"], axis=1, inplace=True)
        predictors.append(predictor_dataset)
    return predictors


def add_predictor(predictor_df, new_predictor):
    return predictor_df.merge(
        new_predictor,
        left_on=["Month", "X", "Y"],
        right_on=["Month", "X", "Y"],
        how="inner",
    )


def build_plankton_tsets(ecosys_dfs):
    cocco_nums, diatom_nums = np.arange(25, 30), np.arange(35, 46)
    cocco_group = ["TRAC" + str(num) for num in cocco_nums]
    diatom_group = ["TRAC" + str(num) for num in diatom_nums]
    cocco_tsets, diatom_tsets = [], []
    for df in ecosys_dfs:
        cocco_tsets.append(sum([df[i] for i in cocco_group]))
        diatom_tsets.append(sum([df[j] for j in diatom_group]))
    return cocco_tsets, diatom_tsets


def apply_size_test_cutoff(cutoff, cocco_tsets, diatom_tsets):
    for i in range(len(cocco_tsets)):
        cocco_tsets[i][cocco_tsets[i] < cutoff] = cutoff
        diatom_tsets[i][diatom_tsets[i] < cutoff] = cutoff
    return cocco_tsets, diatom_tsets


def fit_size_test_gams(cocco_tsets, diatom_tsets, predictor_tsets):
    cocco_gams, diatom_gams = [], []
    for i in range(len(cocco_tsets)):
        cocco_gams.append(
            LinearGAM(n_splines=20).fit(predictor_tsets[i], cocco_tsets[i])
        )
        diatom_gams.append(
            LinearGAM(n_splines=20).fit(predictor_tsets[i], diatom_tsets[i])
        )
    return cocco_gams, diatom_gams


def make_size_test_predictions(name, plankton_gams, predictors_oce):
    """[summary]

    Args:
        plankton_gams ([type]): [description]
        predictors_oce ([type]): [description]

    Returns:
        [dict]:
    """
    predictions_dict = {}
    ocean_X = pd.read_pickle(f"{predictors_oce}")
    for i, gams in enumerate(plankton_gams):
        predictions_dict[f"{name}_{i}"] = gams.predict(ocean_X)
    return predictions_dict

def get_darwin_stats(path, *filenames):
    darwin_stats = []
    for file in filenames:
        try:
            darwin_stats.append(pd.read_pickle(f"{path}/present/{file}.pkl"))
        except:
            darwin_stats.append(pd.read_pickle(f"{path}/future/{file}.pkl"))

    return [darwin_stats[i] for i in range(len(darwin_stats))]