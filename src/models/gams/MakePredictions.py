import numpy as np
import pandas as pd
from pygam import LinearGAM, s, f
import os, sys
from pathlib import Path
import pickle


def make_predictions(plankton_gams, VALIDATION_X):
    predictions_dict = {}
    ocean_X = pd.read_pickle(f"{VALIDATION_X}")
    for group_name, gams in plankton_gams.items():
        predictions_dict[f"{group_name}"] = gams.predict(ocean_X)
    return predictions_dict
