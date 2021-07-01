import os
import numpy as np
from time import sleep
from alive_progress import alive_bar, config_handler
from pathlib import Path
from src.models import Save
from src.models.build_training_sets import TrainingSetBuilder as TSB

ROOT = Path(os.path.abspath(__file__)).parents[2]

# Load
SAMPLES = ROOT / "data" / "interim" / "sampled_ecosys"
OCEAN = ROOT / "data" / "processed" / "model_ocean_data"
# Save
TARGETS_TSETS = Save.check_dir_exists(f"{ROOT}/data/processed/sampled_plankton")
PREDICTORS_TSETS = Save.check_dir_exists(f"{ROOT}/data/processed/sampled_predictors")
VSETS = Save.check_dir_exists(f"{ROOT}/data/processed/validation_sets")


config_handler.set_global(length=50, spinner="fish_bouncing")


print("Obtaining sampled ecosystem and ocean physics data ...")
with alive_bar(2) as bar:
    eco_samp, eco_samp_r, eco_samp_f, eco_samp_rf = TSB.get_data(
        f"{SAMPLES}",
        *[
            "eco_samp_p.pkl",
            "rand_eco_samp_p.pkl",
            "eco_samp_f.pkl",
            "rand_eco_samp_f.pkl",
        ],
    )
    r2_samp, r3_samp, r2_samp_f, r3_samp_f = TSB.get_data(
        f"{SAMPLES}",
        *[
            "r2_samp.pkl",
            "r3_samp.pkl",
            "r2_samp_f.pkl",
            "r3_samp_f.pkl",
        ],
    )
    bar()
    sleep(2)
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
    sleep(2)

print("Building predictor variable training sets (primary) ...")
with alive_bar(5) as bar:
    predictors = TSB.return_predictor_dataset(eco_samp, salinity_oce, sst_oce, par_oce)
    bar()
    sleep(2)
    predictors_r = TSB.return_predictor_dataset(
        eco_samp_r, salinity_oce, sst_oce, par_oce
    )
    bar()
    sleep(2)
    predictors_f = TSB.return_predictor_dataset(
        eco_samp_f, salinity_oce_f, sst_oce_f, par_oce
    )
    bar()
    sleep(2)
    predictors_rf = TSB.return_predictor_dataset(
        eco_samp_rf, salinity_oce_f, sst_oce_f, par_oce
    )
    bar()
    sleep(2)
    Save.save_to_pkl(
        Save.check_dir_exists(f"{PREDICTORS_TSETS}"),
        **{
            "predictors.pkl": predictors,
            "predictors_r.pkl": predictors_r,
            "predictors_f.pkl": predictors_f,
            "predictors_rf.pkl": predictors_rf,
        },
    )
    bar()
    sleep(2)

print("Building predictor variable training sets (using larger random samples) ...")
with alive_bar(4) as bar:
    r2_predictors = TSB.return_predictor_dataset(
        r2_samp, salinity_oce, sst_oce, par_oce
    )
    bar()
    sleep(2)
    r3_predictors = TSB.return_predictor_dataset(
        r3_samp, salinity_oce, sst_oce, par_oce
    )
    bar()
    sleep(2)
    r2_predictors_f = TSB.return_predictor_dataset(
        r2_samp_f, salinity_oce_f, sst_oce_f, par_oce
    )
    bar()
    sleep(2)
    r3_predictors_f = TSB.return_predictor_dataset(
        r3_samp_f, salinity_oce_f, sst_oce_f, par_oce
    )
    bar()
    sleep(2)
    Save.save_to_pkl(
        Save.check_dir_exists(f"{PREDICTORS_TSETS}"),
        **{
            "r2_predictors.pkl": r2_predictors,
            "r3_predictors.pkl": r3_predictors,
            "r2_predictors_f.pkl": r2_predictors_f,
            "r3_predictors_f.pkl": r3_predictors_f,
        },
    )

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
    sleep(2)

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
    sleep(2)

print("Building large test random sets for plankton functional groups...")
with alive_bar(2) as bar:
    r2_pro, r3_pro, r2_pro_f, r3_pro_f = TSB.group_plankton(
        r2_samp, r3_samp, r2_samp_f, r3_samp_f, 21, 22
    )
    r2_pico, r3_pico, r2_pico_f, r3_pico_f = TSB.group_plankton(
        r2_samp, r3_samp, r2_samp_f, r3_samp_f, 23, 24
    )
    r2_cocco, r3_cocco, r2_cocco_f, r3_cocco_f = TSB.group_plankton(
        r2_samp, r3_samp, r2_samp_f, r3_samp_f, *np.arange(25, 30)
    )
    r2_diazo, r3_diazo, r2_diazo_f, r3_diazo_f = TSB.group_plankton(
        r2_samp, r3_samp, r2_samp_f, r3_samp_f, *np.arange(30, 35)
    )
    r2_diatom, r3_diatom, r2_diatom_f, r3_diatom_f = TSB.group_plankton(
        r2_samp, r3_samp, r2_samp_f, r3_samp_f, *np.arange(35, 46)
    )
    r2_dino, r3_dino, r2_dino_f, r3_dino_f = TSB.group_plankton(
        r2_samp, r3_samp, r2_samp_f, r3_samp_f, *np.arange(46, 56)
    )
    r2_zoo, r3_zoo, r2_zoo_f, r3_zoo_f = TSB.group_plankton(
        r2_samp, r3_samp, r2_samp_f, r3_samp_f, *np.arange(56, 72)
    )
    bar()
    sleep(2)

    r2_tsets = [r2_pro, r2_pico, r2_cocco, r2_diazo, r2_diatom, r2_dino, r2_zoo]
    r3_tsets = [r3_pro, r3_pico, r3_cocco, r3_diazo, r3_diatom, r3_dino, r3_zoo]
    r2_tsets_f = [
        r2_pro_f,
        r2_pico_f,
        r2_cocco_f,
        r2_diazo_f,
        r2_diatom_f,
        r2_dino_f,
        r2_zoo_f,
    ]
    r3_tsets_f = [
        r3_pro_f,
        r3_pico_f,
        r3_cocco_f,
        r3_diazo_f,
        r3_diatom_f,
        r3_dino_f,
        r3_zoo_f,
    ]

    Save.plankton_dicts(
        f"{TARGETS_TSETS}",
        **{
            "r2_plankton": r2_tsets,
            "r3_plankton": r3_tsets,
            "r2_plankton_f": r2_tsets_f,
            "r3_plankton_f": r3_tsets_f,
        },
    )
    bar()
    sleep(2)

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
    sleep(2)
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
    sleep(2)

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
    Save.check_dir_exists(f"{VSETS}/plankton")
    Save.plankton_dicts(
        f"{VSETS}",
        **{
            "plankton/plankton_oce": pl_oce,
            "plankton/plankton_oce_f": pl_oce_f,
        },
    )
    bar()
    sleep(2)

print("Building whole-ocean predictor sets (Darwin ocean 1987-2008, 2079-2100)...")
with alive_bar(2) as bar:
    predictors_oce = TSB.return_predictor_dataset(
        eco_oce, salinity_oce, sst_oce, par_oce
    )
    predictors_oce_f = TSB.return_predictor_dataset(
        eco_oce_f, salinity_oce_f, sst_oce_f, par_oce
    )
    bar()
    sleep(2)
    Save.check_dir_exists(f"{VSETS}/predictors")
    Save.save_to_pkl(
        f"{VSETS}",
        **{
            "predictors/predictors_oce.pkl": predictors_oce,
            "predictors/predictors_oce_f.pkl": predictors_oce_f,
        },
    )
    bar()
    sleep(2)
