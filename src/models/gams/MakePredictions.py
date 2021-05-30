import numpy as np
import pandas as pd
from pygam import LinearGAM, s, f
import os, sys
from pathlib import Path


def make_predictions(plankton_gams, predictors_oce):
    """[summary]

    Args:
        plankton_gams ([type]): [description]
        predictors_oce ([type]): [description]

    Returns:
        [dict]:
    """
    predictions_dict = {}
    ocean_X = pd.read_pickle(f"{predictors_oce}")
    for group_name, gams in plankton_gams.items():
        predictions_dict[f"{group_name}"] = gams.predict(ocean_X)
    return predictions_dict
