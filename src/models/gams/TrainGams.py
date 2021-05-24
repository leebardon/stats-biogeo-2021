import numpy as np
import pandas as pd
import pickle
from pygam import LinearGAM, s, f


def get_plankton(path, *plankton_sets):
    p_sets = []
    for p_set in plankton_sets:
        with open(f"{path}/{p_set}.pkl", "rb") as handle:
            plankton_set = pickle.load(handle)
        p_sets.append(plankton_set)
    return [p_sets[i] for i in range(len(p_sets))]


def get_predictors(path, *filenames):
    data = []
    for name in filenames:
        data.append(pd.read_pickle(f"{path}/{name}.pkl"))
    return [data[i] for i in range(len(data))]


def apply_cutoff(cut_off, *plankton_sets):
    p_sets = []
    for plankton in plankton_sets:
        for funct_group, biomass in plankton.items():
            biomass[biomass < cut_off] = 1.001e-5
        p_sets.append(plankton)
    return [set[i] for i in range(len(p_sets))]


def fit_gams(*plankton_predictor_pairs):
    gams_sets = []
    for plank_dict, predictors in plankton_predictor_pairs:
        gams = {}
        for group_name, biomass in plank_dict.items():
            gams[f"{group_name}"] = LinearGAM().fit(predictors, biomass)
        gams_sets.append(gams)
    return [gams_sets[i] for i in range(len(gams_sets))]
