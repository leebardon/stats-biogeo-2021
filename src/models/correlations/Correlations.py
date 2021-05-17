import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import dcor


def dcorr_df():
    index = ["proko", "pico", "cocco", "diazo", "diatom", "dino", "zoo"]
    cols = ["PO4", "NO3", "Fe", "Si", "SST", "SSS", "PAR"]
    return pd.DataFrame(columns=cols, index=index)


def distance_correlation(predictor, plankton):
    return dcor.distance_correlation(predictor.values, plankton.values)


def calculate_dcorr(predictors, f_groups, cols):
    dcorrs = dcorr_df()
    for groupname, plankton_data in f_groups.items():
        for i in range(len(cols)):
            dcorrs.loc[groupname, cols[i]] = distance_correlation(
                predictors[i], plankton_data
            )
    return dcorrs
