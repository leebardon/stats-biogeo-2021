import os
import time
from alive_progress import alive_bar, config_handler
from pathlib import Path
from src.models import Save
from src.models.gams import TrainGams, MakePredictions
from src.views import PartialDepPlots

ROOT = Path(os.path.abspath(__file__)).parents[2]

# Load
DATA = ROOT / "data_test" / "processed"
# Save
RESULTS = Save.check_dir_exists(f"{ROOT}/results_test/gams_output")
PLOTS = Save.check_dir_exists(f"{ROOT}/results_test/all_plots")
# Const.
CUTOFF = 1.001e-5

config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(2)


print("Obtaining plankton and predictor training datasets...")
with alive_bar(1) as bar:
    (plankton, plankton_r, plankton_f, plankton_rf,) = TrainGams.get_plankton(
        f"{DATA}/sampled_plankton",
        *[
            "plankton",
            "plankton_r",
            "plankton_f",
            "plankton_rf",
        ],
    )
    (predictors, predictors_r, predictors_f, predictors_rf,) = TrainGams.get_predictors(
        f"{DATA}/sampled_predictors",
        *[
            "predictors",
            "predictors_r",
            "predictors_f",
            "predictors_rf",
        ],
    )
    bar()
    t

print("Fitting GAMs to sampled Darwin datasets (1987-2008) ...")
with alive_bar(2) as bar:
    plank_cut, plank_cut_r, plank_cut_f, plank_cut_rf = TrainGams.apply_cutoff(
        CUTOFF, *[plankton, plankton_r, plankton_f, plankton_rf]
    )
    bar()
    t
    gams, gams_r = TrainGams.fit_gams(
        *[
            [plank_cut, predictors],
            [plank_cut_r, predictors_r],
        ]
    )
    bar()
    t


print("Fitting GAMs on 2079-2100 samples to assess stability of relationships...")
with alive_bar(2) as bar:
    gams_f, gams_rf = TrainGams.fit_gams(
        *[
            [plank_cut_f, predictors_f],
            [plank_cut_rf, predictors_rf],
        ]
    )
    bar()
    t
    Save.save_gams(
        Save.check_dir_exists(f"{RESULTS}/fitted_models"),
        **{
            "gams": gams,
            "gams_r": gams_r,
            "gams_f": gams_f,
            "gams_rf": gams_rf,
        },
    )
    bar()
    t


print("Generating partial dependency plots...")
with alive_bar(2) as bar:

    PLOTS_PDP = Save.check_dir_exists(f"{PLOTS}/partial_dep_plots")

    PartialDepPlots.partial_dependency_plots(
        Save.check_dir_exists(f"{PLOTS_PDP}/from_measurements"),
        gams,
        gams_f,
    )
    bar()
    t
    PartialDepPlots.partial_dependency_plots(
        Save.check_dir_exists(f"{PLOTS_PDP}/from_random"),
        gams_r,
        gams_rf,
    )
    bar()
    t


print("Predicting Darwin biogeography (1987-2008) from ocean measurements (1987-2008)")
print(" >>> Have a cup of tea - this could take a while! <<<)")
with alive_bar(1) as bar:
    predictions = MakePredictions.make_predictions(
        gams, f"{DATA}/validation_sets/predictors/predictors_oce.pkl"
    )
    bar()
    t
    time.sleep(60)

print("Predicting Darwin biogeography (1987-2008) from random samples (1987-2008) ")
with alive_bar(1) as bar:
    predictions_r = MakePredictions.make_predictions(
        gams_r, f"{DATA}/validation_sets/predictors/predictors_oce.pkl"
    )
    bar()
    t
    time.sleep(60)

print("Predicting Darwin biogeography (2079-2100) from ocean measurements (1987-2008) ")
with alive_bar(1) as bar:
    predictions_f = MakePredictions.make_predictions(
        gams, f"{DATA}/validation_sets/predictors/predictors_oce_f.pkl"
    )
    bar()
    t
    time.sleep(60)

print("Predicting Darwin biogeography (2079-2100) from random samples (1987-2008) ")
with alive_bar(2) as bar:
    predictions_rf = MakePredictions.make_predictions(
        gams_r, f"{DATA}/validation_sets/predictors/predictors_oce_f.pkl"
    )
    bar()
    t
    Save.save_predictions(
        Save.check_dir_exists(f"{RESULTS}/predictions"),
        **{
            "predictions": predictions,
            "predictions_r": predictions_r,
            "predictions_f": predictions_f,
            "predictions_rf": predictions_rf,
        },
    )
    bar()
    t

