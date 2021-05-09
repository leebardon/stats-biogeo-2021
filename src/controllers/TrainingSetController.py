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

# data paths
SAMPLES = base_path / "data" / "processed" / "model_sampled_data"
DARWIN = base_path / "data" / "processed" / "model_whole_ocean_data"

# save paths
TS_SAVE_PATH = base_path / "training_sets"
PLANKTON_TRAINING_SAVE = base_path / "training_sets" / "plankton"
PLANKTON_VAL_SAVE = base_path / "validation_sets" / "plankton"
PREDICTORS_OCEAN_SAVE = base_path / "validation_sets" / "predictors"


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
    Save.save_to_pkl(training_set, f"{DARWIN}/predictors", "predictors_X_3586.pkl")
    Save.save_to_pkl(
        random_training_set, f"{DARWIN}/predictors", "random_predictors_X_3586.pkl"
    )
    bar()
    t

# This all needs refactored ...
print("Building training sets for plankton functional groups...")
with alive_bar(2) as bar:
    prok, prok_r = TSB.group_plankton(ecosys_samp, 21, 22), TSB.group_plankton(
        ecosys_samp_r, 21, 22
    )
    pico, pico_r = TSB.group_plankton(ecosys_samp, 23, 24), TSB.group_plankton(
        ecosys_samp_r, 23, 24
    )
    cocco, cocco_r = (
        TSB.group_plankton(ecosys_samp, *np.arange(25, 30)),
        TSB.group_plankton(ecosys_samp_r, *np.arange(25, 30)),
    )
    diazo, diazo_r = (
        TSB.group_plankton(ecosys_samp, *np.arange(30, 35)),
        TSB.group_plankton(ecosys_samp_r, *np.arange(30, 35)),
    )
    diatom = TSB.group_plankton(ecosys_samp, *np.arange(35, 46))
    diatom_r = TSB.group_plankton(ecosys_samp_r, *np.arange(35, 46))
    dino = TSB.group_plankton(ecosys_samp, *np.arange(46, 56))
    dino_r = TSB.group_plankton(ecosys_samp_r, *np.arange(46, 56))
    zoo = TSB.group_plankton(ecosys_samp, *np.arange(56, 72))
    zoo_r = TSB.group_plankton(ecosys_samp_r, *np.arange(56, 72))
    bar()
    t
    plank_train_measurements = [prok, pico, cocco, diazo, diatom, dino, zoo]
    plank_train_rand = [
        prok_r,
        pico_r,
        cocco_r,
        diazo_r,
        diatom_r,
        dino_r,
        zoo_r,
    ]
    TSB.save_plankton_sets(
        PLANKTON_TRAINING_SAVE, plankton_train_measurements, "training_measurements"
    )
    TSB.save_plankton_sets(
        PLANKTON_TRAINING_SAVE, plankton_train_random, "training_random"
    )
    bar()
    t


print("Building whole-ocean validation sets for plankton functional groups...")
with alive_bar(3) as bar:
    ecosys_oce = pd.read_pickle(ECOSYS_OCEAN)
    ecosys_oce_f = pd.read_pickle(ECOSYS_OCEAN_FUTURE)
    bar()
    t
    prok_val, prok_val_f = TSB.group_plankton(ecosys_oce, 21, 22), TSB.group_plankton(
        ecosys_oce_f, 21, 22
    )
    pico_val, pico_val_f = TSB.group_plankton(ecosys_oce, 23, 24), TSB.group_plankton(
        ecosys_oce_f, 23, 24
    )
    cocco_val, cocco_val_f = (
        TSB.group_plankton(ecosys_oce, *np.arange(25, 30)),
        TSB.group_plankton(ecosys_oce_f, *np.arange(25, 30)),
    )
    diazo_val, diazo_val_f = (
        TSB.group_plankton(ecosys_oce, *np.arange(30, 35)),
        TSB.group_plankton(ecosys_oce_f, *np.arange(30, 35)),
    )
    diatom_val = TSB.group_plankton(ecosys_oce, *np.arange(35, 46))
    diatom_val_f = TSB.group_plankton(ecosys_oce_f, *np.arange(35, 46))
    dino_val = TSB.group_plankton(ecosys_oce, *np.arange(46, 56))
    dino_val_f = TSB.group_plankton(ecosys_oce_f, *np.arange(46, 56))
    zoo_val = TSB.group_plankton(ecosys_oce, *np.arange(56, 72))
    zoo_val_f = TSB.group_plankton(ecosys_oce_f, *np.arange(56, 72))
    bar()
    t
    plankton_val_present = [
        prok_val,
        pico_val,
        cocco_val,
        diazo_val,
        diatom_val,
        dino_val,
        zoo_val,
    ]
    plankton_val_future = [
        prok_val_f,
        pico_val_f,
        cocco_val_f,
        diazo_val_f,
        diatom_val_f,
        dino_val_f,
        zoo_val_f,
    ]
    TSB.save_plankton_sets(PLANKTON_VAL_SAVE, plankton_val_present, "ocean_present")
    TSB.save_plankton_sets(PLANKTON_VAL_SAVE, plankton_val_future, "ocean_future")
    bar()
    t

print("Building whole-ocean predictor sets (model ocean of 1987-2008 and 2079-2100)...")
with alive_bar(3) as bar:
    salinity_oce_f = pd.read_pickle(SALINITY_OCEAN_FUTURE)
    sst_oce_f = pd.read_pickle(SST_OCEAN_FUTURE)
    bar()
    t
    predictor_set_p = TSB.return_predictor_dataset(
        ecosys_oce, salinity_oce, sst_oce, par
    )
    predictor_set_f = TSB.return_predictor_dataset(
        ecosys_oce_f, salinity_oce_f, sst_oce_f, par
    )
    bar()
    t
    predictor_set_p.to_pickle(f"{PREDICTORS_OCEAN_SAVE}/ocean_X_present.pkl")
    predictor_set_f.to_pickle(f"{PREDICTORS_OCEAN_SAVE}/ocean_X_future.pkl")
    bar()
    t
