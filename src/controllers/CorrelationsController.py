import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import time
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.models.correlations import Correlations

base_path = Path(os.path.abspath(__file__)).parents[2]

TRAINING_SETS = base_path / "data" / "processed"

config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.05)


print("Getting plankton and predictors sample sets...")
with alive_bar(2) as bar:
    plankton, plankton_r, plankton_f, plankton_r_f = Correlations.get_sample_sets(
        f"{TRAINING_SETS}/sampled_ecosys/eco_samp_p.pkl",
        f"{TRAINING_SETS}/sampled_ecosys/rand_eco_samp_p.pkl",
        f"{TRAINING_SETS}/sampled_ecosys/eco_samp_f.pkl",
        f"{TRAINING_SETS}/sampled_ecosys/rand_eco_samp_f.pkl",
    )
    bar()
    t
    (
        predictors,
        predictors_r,
        predictors_f,
        predictors_r_f,
    ) = Correlations.get_sample_sets(
        f"{TRAINING_SETS}/sampled_predictors/predictors_X.pkl",
        f"{TRAINING_SETS}/sampled_predictors/rand_predictors_X.pkl",
        f"{TRAINING_SETS}/sampled_predictors/predictors_X_f.pkl",
        f"{TRAINING_SETS}/sampled_predictors/rand_predictors_X_f.pkl",
    )
    bar()
    t

print("Calculating distance correlations...")
with alive_bar(4) as bar:
    dcorrs = Correlations.calculate_dcorrs(predictors, plankton)
    bar()
    t
    dcorrs_r = Correlations.calculate_dcorrs(predictors_r, plankton_r)
    bar()
    t
    dcorrs_f = Correlations.calculate_dcorrs(predictors_f, plankton_f)
    bar()
    t
    dcorrs_r_f = Correlations.calculate_dcorrs(predictors_r_f, plankton_r_f)
    bar()
    t
