import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import numpy as np
import pandas as pd
import pickle
import time
from alive_progress import alive_bar, config_handler
from pathlib import Path
from pygam import LinearGAM, s, f
from src.models.gams import TrainGams, MakePredictions
from src.views import PartialDepPlots

base_path = Path(os.path.abspath(__file__)).parents[2]

T_SETS = base_path / "data" / "processed" / "training_sets"
V_SETS = base_path / "data" / "processed" / "validation_sets"
RESULTS = base_path / "results" / "gams_output"
PLOTS = base_path / "results" / "all_plots"

config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.05)


print("Obtaining plankton and predictor training datasets...")
with alive_bar(1) as bar:
    with open(f"{T_SETS}/plankton/plankton_training_measurements.pkl", "rb") as handle:
        plankton = pickle.load(handle)
    with open(f"{T_SETS}/plankton/plankton_training_random.pkl", "rb") as handle:
        plankton_random = pickle.load(handle)

    predictors, predictors_random = TrainGams.get_predictors(f"{T_SETS}/predictors")
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
        f"{RESULTS}/fitted_models/from_measurements/gams_dict.pkl", "wb"
    ) as handle:
        pickle.dump(plankton_gams_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open(f"{RESULTS}/fitted_models/from_random/gams_r_dict.pkl", "wb") as handle:
        pickle.dump(plankton_random_gams_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    bar()
    t


print("Generating partial dependency plots...")
with alive_bar(2) as bar:
    PartialDepPlots.partial_dependency_plots(
        predictors,
        plankton_gams_dict,
        f"{PLOTS}/partial_dep_plots/from_measurements",
    )
    bar()
    t
    PartialDepPlots.partial_dependency_plots(
        predictors,
        plankton_random_gams_dict,
        f"{PLOTS}/partial_dep_plots/from_random",
    )
    bar()
    t

print("\n")
print("Using GAMs from measurements to predict Darwin ocean biogeography (1987-2008)")
print("(Have a cup of tea - this could take a while...)")
with alive_bar(1) as bar:
    predictions_present = MakePredictions.make_predictions(
        plankton_gams_dict, f"{V_SETS}/predictors/ocean_X_present.pkl"
    )
    with open(f"{RESULTS}/predictions_present/predictions_p.pkl", "wb") as handle:
        pickle.dump(predictions_present, handle, protocol=pickle.HIGHEST_PROTOCOL)
    bar()
    t

print(
    "Using GAMs from random sampling to predict Darwin ocean biogeography (1987-2008)"
)
with alive_bar(1) as bar:
    predictions_present_r = MakePredictions.make_predictions(
        plankton_random_gams_dict, f"{V_SETS}/predictors/ocean_X_present.pkl"
    )
    with open(
        f"{RESULTS}/predictions_present/predictions_random_p.pkl", "wb"
    ) as handle:
        pickle.dump(predictions_present_r, handle, protocol=pickle.HIGHEST_PROTOCOL)
    bar()
    t

print("Using GAMs from measurements to predict Darwin ocean biogeography (2079-2100)")
with alive_bar(1) as bar:
    predictions_future = MakePredictions.make_predictions(
        plankton_gams_dict, f"{V_SETS}/predictors/ocean_X_future.pkl"
    )
    with open(f"{RESULTS}/predictions_future/predictions_f.pkl", "wb") as handle:
        pickle.dump(predictions_future, handle, protocol=pickle.HIGHEST_PROTOCOL)
    bar()
    t

print(
    "Using GAMs from random sampling to predict Darwin ocean biogeography (2079-2100)"
)
with alive_bar(1) as bar:
    predictions_future_r = MakePredictions.make_predictions(
        plankton_random_gams_dict, f"{V_SETS}/predictors/ocean_X_future.pkl"
    )
    with open(f"{RESULTS}/predictions_future/predictions_f.pkl", "wb") as handle:
        pickle.dump(predictions_future_r, handle, protocol=pickle.HIGHEST_PROTOCOL)
    bar()
    t
