import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import dcor


def get_sample_sets(*paths):
    sets = {}
    for i in range(0, len(paths)):
        sets[f"s{i}"] = pd.read_pickle(paths[i])
    return [sets[f"s{i}"] for i in range(0, len(sets))]


def calculate_dcorrs(predictors, f_groups):
    dcorrs = dcorr_df()
    cols = ["PO4", "NO3", "Fe", "Si", "SST", "SSS", "PAR"]
    predictors[["PAR", "SSS", "SST"]] = np.float64(predictors[["PAR", "SSS", "SST"]])
    predictors.reset_index(drop=True, inplace=True)
    for groupname, plankton_data in f_groups.items():
        for i in range(len(cols)):
            dcorrs.loc[groupname, cols[i]] = distance_correlation(
                predictors[cols[i]].values, plankton_data.values
            )
    return dcorrs


def dcorr_df():
    index = ["Pro", "Pico", "Cocco", "Diazo", "Diatom", "Dino", "Zoo"]
    cols = ["PO4", "NO3", "Fe", "Si", "SST", "SSS", "PAR"]
    return pd.DataFrame(columns=cols, index=index)


def distance_correlation(predictor, plankton):
    return dcor.distance_correlation(predictor, plankton)
