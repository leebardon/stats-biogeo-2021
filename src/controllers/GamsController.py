import numpy as np
import pandas as pd
from alive_progress import alive_bar, config_handler
import time
import os, sys
import pickle
from pathlib import Path
from pygam import LinearGAM, s, f

from ML_Biogeography_2021.models.gams import TrainGams, MakePredictions
from ML_Biogeography_2021.models.generate_plots import PartialDepPlots

base_path = Path(os.path.abspath(__file__)).parents[1] / "all_outputs"

PLANKTON_PATH = base_path / "training_sets" / "plankton"
PREDICTORS_PATH = base_path / "training_sets" / "predictors"
PREDICTORS_OCEAN_X = (
    base_path / "validation_sets" / "predictors" / "ocean_X_present.pkl"
)
PREDICTORS_OCEAN_X_F = (
    base_path / "validation_sets" / "predictors" / "ocean_X_future.pkl"
)
GAMS_SAVE_PATH = base_path / "gams_output"
PLOTS_SAVE_PATH = base_path / "all_plots"
PREDICTIONS_SAVE_P = base_path / "gams_output" / "predictions_present"
PREDICTIONS_SAVE_F = base_path / "gams_output" / "predictions_future"

config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.05)


print("Obtaining plankton and predictor training datasets...")
with alive_bar(1) as bar:
    with open(f"{PLANKTON_PATH}/plankton_training_measurements.pkl", "rb") as handle:
        plankton = pickle.load(handle)
    with open(f"{PLANKTON_PATH}/plankton_training_random.pkl", "rb") as handle:
        plankton_random = pickle.load(handle)

    predictors, predictors_random = TrainGams.get_predictors(PREDICTORS_PATH)
    bar()
    t

print("Fitting generalised additive models...")
with alive_bar(3) as bar:
    plankton = TrainGams.set_min_vals(plankton)
    plankton_random = TrainGams.set_min_vals(plankton_random)
    bar()
    t
    plankton_gams_dict = TrainGams.fit_gams(plankton, predictors)
    plankton_random_gams_dict = TrainGams.fit_gams(plankton_random, predictors_random)
    bar()
    t
    with open(
        f"{GAMS_SAVE_PATH}/fitted_models/from_measurements/gams_dict.pkl", "wb"
    ) as handle:
        pickle.dump(plankton_gams_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(
        f"{GAMS_SAVE_PATH}/fitted_models/from_random/gams_r_dict.pkl", "wb"
    ) as handle:
        pickle.dump(plankton_random_gams_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    bar()
    t


print("Generating partial dependency plots...")
with alive_bar(2) as bar:
    PartialDepPlots.partial_dependency_plots(
        predictors, plankton_gams_dict, PLOTS_SAVE_PATH, pathnum=1
    )
    bar()
    t
    PartialDepPlots.partial_dependency_plots(
        predictors, plankton_random_gams_dict, PLOTS_SAVE_PATH, pathnum=2
    )
    bar()
    t

print("\n")
print("Using GAMs from measurements to predict Darwin ocean biogeography (1987-2008)")
print("(Have a cup of tea - this could take a while...)")
with alive_bar(1) as bar:
    predictions_present = MakePredictions.make_predictions(
        plankton_gams_dict, PREDICTORS_OCEAN_X
    )
    with open(f"{PREDICTIONS_SAVE_P}/predictions_p.pkl", "wb") as handle:
        pickle.dump(predictions_present, handle, protocol=pickle.HIGHEST_PROTOCOL)
    bar()
    t

print(
    "Using GAMs from random sampling to predict Darwin ocean biogeography (1987-2008)"
)
with alive_bar(1) as bar:
    predictions_present_r = MakePredictions.make_predictions(
        plankton_random_gams_dict, PREDICTORS_OCEAN_X
    )
    with open(f"{PREDICTIONS_SAVE_P}/predictions_random_p.pkl", "wb") as handle:
        pickle.dump(predictions_present_r, handle, protocol=pickle.HIGHEST_PROTOCOL)
    bar()
    t

print("Using GAMs from measurements to predict Darwin ocean biogeography (2079-2100)")
with alive_bar(1) as bar:
    predictions_future = MakePredictions.make_predictions(
        plankton_gams_dict, PREDICTORS_OCEAN_X_F
    )
    with open(f"{PREDICTIONS_SAVE_F}/predictions_f.pkl", "wb") as handle:
        pickle.dump(predictions_future, handle, protocol=pickle.HIGHEST_PROTOCOL)
    bar()
    t

print(
    "Using GAMs from random sampling to predict Darwin ocean biogeography (2079-2100)"
)
with alive_bar(1) as bar:
    predictions_future_r = MakePredictions.make_predictions(
        plankton_random_gams_dict, PREDICTORS_OCEAN_X_F
    )
    with open(f"{PREDICTIONS_SAVE_F}/predictions_random_f.pkl", "wb") as handle:
        pickle.dump(predictions_future_r, handle, protocol=pickle.HIGHEST_PROTOCOL)
    bar()
    t
