import numpy as np
import pandas as pd
from pygam import LinearGAM, s, f


def get_plankton(path):
    plankton_dict = {
        "proko": pd.read_pickle(f"{path}/proko.pkl"),
        "pico": pd.read_pickle(f"{path}/pico.pkl"),
        "cocco": pd.read_pickle(f"{path}/cocco.pkl"),
        "diazo": pd.read_pickle(f"{path}/diazo.pkl"),
        "diatom": pd.read_pickle(f"{path}/diatom.pkl"),
        "dino": pd.read_pickle(f"{path}/dino.pkl"),
        "zoo": pd.read_pickle(f"{path}/zoo.pkl"),
    }
    return plankton_dict


def get_predictors(path):
    predictors = pd.read_pickle(f"{path}/predictors_X_3586.pkl")
    predictors_random = pd.read_pickle(f"{path}/random_predictors_X_3586.pkl")
    return predictors, predictors_random


def set_min_vals(plankton):
    for group_name, biomass in plankton.items():
        biomass[biomass < 1.001e-5] = 1.001e-5
    return plankton


def fit_gams(plankton, predictors):
    gams_dict = {}
    for group_name, biomass in plankton.items():
        gams_dict[f"{group_name}"] = LinearGAM().fit(predictors, biomass)
    return gams_dict
