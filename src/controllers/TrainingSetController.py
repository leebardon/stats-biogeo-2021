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

SAMPLES = base_path / "data" / "interim" / "sampled_ecosys"
OCEAN = base_path / "data" / "processed" / "model_ocean_data"
TARGETS_TSETS = base_path / "data" / "processed" / "sampled_plankton"
PREDICTORS_TSETS = base_path / "data" / "processed" / "sampled_predictors"
VSETS = base_path / "data" / "processed" / "validation_sets"


config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(1)


print("Building predictor variable training sets...")
with alive_bar(6) as bar:
    eco_samp, eco_samp_r, eco_samp_f, eco_samp_rf = TSB.get_data(
        f"{SAMPLES}",
        *[
            "eco_samp_p.pkl",
            "rand_eco_samp_p.pkl",
            "eco_samp_f.pkl",
            "rand_eco_samp_f.pkl",
        ],
    )
    salinity_oce, sst_oce, par_oce = TSB.get_data(
        f"{OCEAN}/present",
        *[
            "sss_ocean_p.pkl",
            "sst_ocean_p.pkl",
            "par_ocean.pkl",
        ],
    )
    salinity_oce_f, sst_oce_f, par_oce = TSB.get_data(
        f"{OCEAN}/future",
        *[
            "sss_ocean_f.pkl",
            "sst_ocean_f.pkl",
            "par_ocean.pkl",
        ],
    )
    bar()
    t
    predictors = TSB.return_predictor_dataset(eco_samp, salinity_oce, sst_oce, par_oce)
    bar()
    t
    predictors_r = TSB.return_predictor_dataset(
        eco_samp_r, salinity_oce, sst_oce, par_oce
    )
    bar()
    t
    predictors_f = TSB.return_predictor_dataset(
        eco_samp_f, salinity_oce_f, sst_oce_f, par_oce
    )
    bar()
    t
    predictors_rf = TSB.return_predictor_dataset(
        eco_samp_rf, salinity_oce_f, sst_oce_f, par_oce
    )
    bar()
    t
    Save.save_to_pkl(
        f"{PREDICTORS_TSETS}",
        **{
            "predictors.pkl": predictors,
            "predictors_r.pkl": predictors_r,
            "predictors_f.pkl": predictors_f,
            "predictors_rf.pkl": predictors_rf,
        },
    )
    bar()
    t

print("Building training sets for plankton functional groups...")
with alive_bar(2) as bar:
    pro, pro_r, pro_f, pro_rf = TSB.group_plankton(
        eco_samp, eco_samp_r, eco_samp_f, eco_samp_rf, 21, 22
    )
    pico, pico_r, pico_f, pico_rf = TSB.group_plankton(
        eco_samp, eco_samp_r, eco_samp_f, eco_samp_rf, 23, 24
    )
    cocco, cocco_r, cocco_f, cocco_rf = TSB.group_plankton(
        eco_samp, eco_samp_r, eco_samp_f, eco_samp_rf, *np.arange(25, 30)
    )
    diazo, diazo_r, diazo_f, diazo_rf = TSB.group_plankton(
        eco_samp, eco_samp_r, eco_samp_f, eco_samp_rf, *np.arange(30, 35)
    )
    diatom, diatom_r, diatom_f, diatom_rf = TSB.group_plankton(
        eco_samp, eco_samp_r, eco_samp_f, eco_samp_rf, *np.arange(35, 46)
    )
    dino, dino_r, dino_f, dino_rf = TSB.group_plankton(
        eco_samp, eco_samp_r, eco_samp_f, eco_samp_rf, *np.arange(46, 56)
    )
    zoo, zoo_r, zoo_f, zoo_rf = TSB.group_plankton(
        eco_samp, eco_samp_r, eco_samp_f, eco_samp_rf, *np.arange(56, 72)
    )
    bar()
    t

    pl_tsets = [pro, pico, cocco, diazo, diatom, dino, zoo]
    pl_tsets_r = [pro_r, pico_r, cocco_r, diazo_r, diatom_r, dino_r, zoo_r]
    pl_tsets_f = [pro_f, pico_f, cocco_f, diazo_f, diatom_f, dino_f, zoo_f]
    pl_tsets_rf = [pro_rf, pico_rf, cocco_rf, diazo_rf, diatom_rf, dino_rf, zoo_rf]

    Save.plankton_dicts(
        f"{TARGETS_TSETS}",
        **{
            "plankton": pl_tsets,
            "plankton_r": pl_tsets_r,
            "plankton_f": pl_tsets_f,
            "plankton_rf": pl_tsets_rf,
        },
    )
    bar()
    t

print("Building whole-ocean validation sets for plankton functional groups...")
with alive_bar(3) as bar:
    eco_oce, eco_oce_f = TSB.get_data(
        f"{OCEAN}",
        *[
            "present/ecosys_ocean_p.pkl",
            "future/ecosys_ocean_f.pkl",
        ],
    )
    bar()
    t
    pro_oce, pro_oce_f = TSB.group_oce_plank(eco_oce, eco_oce_f, 21, 22)
    pico_oce, pico_oce_f = TSB.group_oce_plank(eco_oce, eco_oce_f, 23, 24)
    cocco_oce, cocco_oce_f = TSB.group_oce_plank(eco_oce, eco_oce_f, *np.arange(25, 30))
    diazo_oce, diazo_oce_f = TSB.group_oce_plank(eco_oce, eco_oce_f, *np.arange(30, 35))
    diatom_oce, diatom_oce_f = TSB.group_oce_plank(
        eco_oce, eco_oce_f, *np.arange(35, 46)
    )
    dino_oce, dino_oce_f = TSB.group_oce_plank(eco_oce, eco_oce_f, *np.arange(46, 56))
    zoo_oce, zoo_oce_f = TSB.group_oce_plank(eco_oce, eco_oce_f, *np.arange(56, 72))
    bar()
    t

    pl_oce = [pro_oce, pico_oce, cocco_oce, diazo_oce, diatom_oce, dino_oce, zoo_oce]
    pl_oce_f = [
        pro_oce_f,
        pico_oce_f,
        cocco_oce_f,
        diazo_oce_f,
        diatom_oce_f,
        dino_oce_f,
        zoo_oce_f,
    ]

    Save.plankton_dicts(
        f"{VSETS}",
        **{
            "plankton/plankton_oce.pkl": pl_oce,
            "plankton/plankton_oce_f.pkl": pl_oce_f,
        },
    )
    bar()
    t

print("Building whole-ocean predictor sets (Darwin ocean 1987-2008, 2079-2100)...")
with alive_bar(2) as bar:
    predictors_oce_X = TSB.return_predictor_dataset(
        eco_oce, salinity_oce, sst_oce, par_oce
    )
    predictors_oce_Xf = TSB.return_predictor_dataset(
        eco_oce_f, salinity_oce_f, sst_oce_f, par_oce
    )
    bar()
    t
    Save.save_to_pkl(
        f"{VSETS}",
        **{
            "predictors/predictors_oce_X.pkl": predictors_oce_X,
            "predictors/predictors_oce_Xf.pkl": predictors_oce_Xf,
        },
    )
    bar()
    t
