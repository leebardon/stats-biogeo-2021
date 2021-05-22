import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dcor

COLS = ["PO4", "NO3", "Fe", "Si", "SST", "SSS", "PAR"]
INDEX = ["Pro", "Pico", "Cocco", "Diazo", "Diatom", "Dino", "Zoo"]


def get_sample_sets(*paths):
    sets = {}
    for i in range(0, len(paths)):
        sets[f"s{i}"] = pd.read_pickle(paths[i])
    return [sets[f"s{i}"] for i in range(0, len(sets))]


def calculate_dcorrs(predictors, f_groups):
    dcorrs = dcorr_df()
    predictors[["PAR", "SSS", "SST"]] = np.float64(predictors[["PAR", "SSS", "SST"]])
    predictors.reset_index(drop=True, inplace=True)
    for groupname, plankton_data in f_groups.items():
        for i in range(len(COLS)):
            dcorrs.loc[groupname, COLS[i]] = distance_correlation(
                predictors[COLS[i]].values, plankton_data.values
            )
    return dcorrs


def dcorr_df():
    return pd.DataFrame(columns=COLS, index=INDEX)


def distance_correlation(predictor, plankton):
    return dcor.distance_correlation(predictor, plankton)


def calculate_pearsons(predictors, plankton):
    pear_df = get_df(predictors, plankton)
    pearsons = pear_df.corr(method="pearson")
    pearsons_trimmed = pearsons[INDEX].iloc[0:7]
    return pearsons_trimmed.T


def calculate_ln_pearsons(predictors, plankton):
    pear_df = get_df(predictors, plankton)
    ln_pear_df = np.log(pear_df)
    ln_pearsons = ln_pear_df.corr(method="pearson")
    ln_pearsons_trimmed = ln_pearsons[INDEX].iloc[0:7]
    return ln_pearsons_trimmed.T


def calculate_spearmans(predictors, plankton):
    spear_df = get_df(predictors, plankton)
    spearmans = spear_df.corr(method="spearman")
    spearmans_trimmed = spearmans[INDEX].iloc[0:7]
    return spearmans_trimmed.T


def get_df(predictors, plankton):
    plank_df = pd.DataFrame(plankton, columns=INDEX)
    return pd.concat([predictors, plank_df], axis=1)
