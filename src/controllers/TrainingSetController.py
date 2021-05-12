import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import numpy as np
import pandas as pd
import xarray as xr
import time
from alive_progress import alive_bar, config_handler
from pathlib import Path
from src.models import Save
from src.models.build_training_sets import TrainingSetBuilder as TSB

base_path = Path(os.path.abspath(__file__)).parents[2]

SAMPLES = base_path / "data" / "processed" / "model_sampled_data"
DARWIN = base_path / "data" / "processed" / "model_ocean_data"
T_SET = base_path / "data" / "processed" / "training_sets"
V_SET = base_path / "data" / "processed" / "validation_sets"

config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.05)


print("Building predictor variable training sets...")
with alive_bar(4) as bar:
    ecosys_samp = pd.read_pickle(f"{SAMPLES}/ecosys_sample_3586.pkl")
    ecosys_samp_r = pd.read_pickle(f"{SAMPLES}/random_ecosys_sample_3586.pkl")
    bar()
    t
    salinity_oce = pd.read_pickle(f"{DARWIN}/present/sss_ocean_p.pkl")
    sst_oce = pd.read_pickle(f"{DARWIN}/present/sst_ocean_p.pkl")
    par = pd.read_pickle(f"{DARWIN}/par_ocean.pkl")
    bar()
    t
    training_set = TSB.return_predictor_dataset(ecosys_samp, salinity_oce, sst_oce, par)
    random_training_set = TSB.return_predictor_dataset(
        ecosys_samp_r, salinity_oce, sst_oce, par
    )
    bar()
    Save.save_to_pkl(training_set, f"{T_SET}/predictors", "predictors_X_3586.pkl")
    Save.save_to_pkl(
        random_training_set, f"{T_SET}/predictors", "random_predictors_X_3586.pkl"
    )
    bar()
    t

# # This all needs refactored ...
# print("Building training sets for plankton functional groups...")
# with alive_bar(2) as bar:
#     prok, prok_r = TSB.group_plankton(ecosys_samp, 21, 22), TSB.group_plankton(
#         ecosys_samp_r, 21, 22
#     )
#     pico, pico_r = TSB.group_plankton(ecosys_samp, 23, 24), TSB.group_plankton(
#         ecosys_samp_r, 23, 24
#     )
#     cocco, cocco_r = (
#         TSB.group_plankton(ecosys_samp, *np.arange(25, 30)),
#         TSB.group_plankton(ecosys_samp_r, *np.arange(25, 30)),
#     )
#     diazo, diazo_r = (
#         TSB.group_plankton(ecosys_samp, *np.arange(30, 35)),
#         TSB.group_plankton(ecosys_samp_r, *np.arange(30, 35)),
#     )
#     diatom = TSB.group_plankton(ecosys_samp, *np.arange(35, 46))
#     diatom_r = TSB.group_plankton(ecosys_samp_r, *np.arange(35, 46))
#     dino = TSB.group_plankton(ecosys_samp, *np.arange(46, 56))
#     dino_r = TSB.group_plankton(ecosys_samp_r, *np.arange(46, 56))
#     zoo = TSB.group_plankton(ecosys_samp, *np.arange(56, 72))
#     zoo_r = TSB.group_plankton(ecosys_samp_r, *np.arange(56, 72))
#     bar()
#     t
#     plank_train_meas = TSB.get_arr(type=1)
#     plank_train_rand = TSB.get_arr(type=2)
#     Save.plankton_sets(f"{T_SET}/plankton", plank_train_meas, "training_measurements")
#     Save, plankton_sets(f"{T_SET}/plankton", plank_train_rand, "training_random")
#     bar()
#     t


# print("Building whole-ocean validation sets for plankton functional groups...")
# with alive_bar(3) as bar:
#     ecosys_oce = pd.read_pickle(f"{DARWIN}/present/ecosys_ocean_p.pkl")
#     ecosys_oce_f = pd.read_pickle(f"{DARWIN}/future/ecosys_ocean_f.pkl")
#     bar()
#     t
#     prok_val, prok_val_f = TSB.group_plankton(ecosys_oce, 21, 22), TSB.group_plankton(
#         ecosys_oce_f, 21, 22
#     )
#     pico_val, pico_val_f = TSB.group_plankton(ecosys_oce, 23, 24), TSB.group_plankton(
#         ecosys_oce_f, 23, 24
#     )
#     cocco_val, cocco_val_f = (
#         TSB.group_plankton(ecosys_oce, *np.arange(25, 30)),
#         TSB.group_plankton(ecosys_oce_f, *np.arange(25, 30)),
#     )
#     diazo_val, diazo_val_f = (
#         TSB.group_plankton(ecosys_oce, *np.arange(30, 35)),
#         TSB.group_plankton(ecosys_oce_f, *np.arange(30, 35)),
#     )
#     diatom_val = TSB.group_plankton(ecosys_oce, *np.arange(35, 46))
#     diatom_val_f = TSB.group_plankton(ecosys_oce_f, *np.arange(35, 46))
#     dino_val = TSB.group_plankton(ecosys_oce, *np.arange(46, 56))
#     dino_val_f = TSB.group_plankton(ecosys_oce_f, *np.arange(46, 56))
#     zoo_val = TSB.group_plankton(ecosys_oce, *np.arange(56, 72))
#     zoo_val_f = TSB.group_plankton(ecosys_oce_f, *np.arange(56, 72))
#     bar()
#     t
#     plank_val_pres = TSB.get_arr(type=3)
#     plank_val_fut = TSB.get_arr(type=4)
#     Save.plankton_sets(f"{V_SET}/plankton", plank_val_pres, "ocean_present")
#     Save.plankton_sets(f"{V_SET}/plankton", plank_val_fut, "ocean_future")
#     bar()
#     t

# print(
#     "Building whole-ocean predictor sets (Darwin ocean of 1987-2008 and 2079-2100)..."
# )
# with alive_bar(2) as bar:
#     salinity_oce_f = pd.read_pickle(f"{DARWIN}/future/sss_ocean_f.pkl")
#     sst_oce_f = pd.read_pickle(f"{DARWIN}/future/sst_ocean_f.pkl")
#     bar()
#     t
#     predictor_set_p = TSB.return_predictor_dataset(
#         ecosys_oce, salinity_oce, sst_oce, par
#     )
#     predictor_set_f = TSB.return_predictor_dataset(
#         ecosys_oce_f, salinity_oce_f, sst_oce_f, par
#     )
#     Save.save_to_pkl(predictor_set_p, f"{V_SET}/predictors", "ocean_X_present.pkl")
#     Save.save_to_pkl(predictor_set_f, f"{V_SET}/predictors", "ocean_X_future.pkl")
#     bar()
#     t
