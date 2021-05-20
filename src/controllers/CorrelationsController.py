import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import time
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.models.correlations import Dcorrs
from src.models import Save

BASEPATH = Path(os.path.abspath(__file__)).parents[2]
DATASETS = f"{BASEPATH}/data/processed"
SAVEPATH = Save.check_dir_exists(f"{DATASETS}/correlations")

config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.05)


print("Getting plankton and predictors sample sets...")
with alive_bar(2) as bar:
    plankton, plankton_r, plankton_f, plankton_r_f = Dcorrs.get_sample_sets(
        f"{DATASETS}/sampled_plankton/plankton.pkl",
        f"{DATASETS}/sampled_plankton/plankton_r.pkl",
        f"{DATASETS}/sampled_plankton/plankton_f.pkl",
        f"{DATASETS}/sampled_plankton/plankton_r_f.pkl",
    )
    bar()
    t
    (predictors, predictors_r, predictors_f, predictors_r_f,) = Dcorrs.get_sample_sets(
        f"{DATASETS}/sampled_predictors/predictors_X.pkl",
        f"{DATASETS}/sampled_predictors/rand_predictors_X.pkl",
        f"{DATASETS}/sampled_predictors/predictors_X_f.pkl",
        f"{DATASETS}/sampled_predictors/rand_predictors_X_f.pkl",
    )
    bar()
    t

print("Calculating distance correlations...")
with alive_bar(4) as bar:
    dcorrs = Dcorrs.calculate_dcorrs(predictors, plankton)
    Save.save_to_pkl(f"{SAVEPATH}/dcorrs", **{"dcorrs.pkl": dcorrs})
    bar()
    t
    dcorrs_r = Dcorrs.calculate_dcorrs(predictors_r, plankton_r)
    Save.save_to_pkl(f"{SAVEPATH}/dcorrs", **{"dcorrs_r.pkl": dcorrs_r})
    bar()
    t
    dcorrs_f = Dcorrs.calculate_dcorrs(predictors_f, plankton_f)
    Save.save_to_pkl(f"{SAVEPATH}/dcorrs", **{"dcorrs_f.pkl": dcorrs_f})
    bar()
    t
    dcorrs_r_f = Dcorrs.calculate_dcorrs(predictors_r_f, plankton_r_f)
    Save.save_to_pkl(f"{SAVEPATH}/dcorrs", **{"dcorrs_r_f.pkl": dcorrs_r_f})
    bar()
    t
