import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import time
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.models.gams import AnalyseGams
from src.models import Save

base_path = Path(os.path.abspath(__file__)).parents[2]
PREDICTIONS = base_path / "results" / "gams_output" / "predictions"
TARGETS = base_path / "data" / "processed" / "validation_sets" / "plankton"
ANALYSIS_SAVE = base_path / "results" / "analysis_output"


config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.05)


print("Getting GAMs predictions and Darwin target data...")
with alive_bar(2) as bar:
    (
        predictions,
        predictions_r,
        predictions_f,
        predictions_rf,
    ) = AnalyseGams.get_predictions(
        f"{PREDICTIONS}",
        *[
            "predictions",
            "predictions_r",
            "predictions_f",
            "predictions_rf",
        ],
    )
    bar()
    t
    (darwin_ocean, darwin_ocean_f,) = AnalyseGams.get_targets(
        f"{TARGETS}",
        *[
            "darwin_ocean",
            "darwin_ocean_f",
        ],
    )
    bar()
    t


print(
    "Applying presence-absence cut-off, calculating false positives and negatives ..."
)
with alive_bar(5) as bar:
    predictions_cut, darwin_cut, cutoff_summary = AnalyseGams.cut_off(
        predictions, darwin_ocean, 1.001e-5
    )
    bar()
    t
    predictions_cut_r, darwin_cut_r, cutoff_summary_r = AnalyseGams.cut_off(
        predictions_r, darwin_ocean, 1.001e-5
    )
    bar()
    t
    predictions_cut_f, darwin_cut_f, cutoff_summary_f = AnalyseGams.cut_off(
        predictions_f, darwin_ocean_f, 1.001e-5
    )
    bar()
    t
    predictions_cut_rf, darwin_cut_rf, cutoff_summary_rf = AnalyseGams.cut_off(
        predictions_rf, darwin_ocean_f, 1.001e-5
    )
    bar()
    t
    Save.save_with_cutoff_removed(
        ANALYSIS_SAVE,
        predictions_cut,
        predictions_cut_r,
        darwin_cut,
        predictions_cut_f,
        predictions_cut_rf,
        darwin_cut_f,
    )
    bar()
    t

print("Calculating mean and median biomasses for each functional group (1987-2008)...")
with alive_bar(4) as bar:
    mean_predictions, median_predictions = AnalyseGams.mean_and_median(
        predictions_cut, [], []
    )
    bar()
    t
    mean_predictions_r, median_predictions_r = AnalyseGams.mean_and_median(
        predictions_cut_r, [], []
    )
    bar()
    t
    mean_darwin, median_darwin = AnalyseGams.mean_and_median(darwin_cut, [], [])
    bar()
    t

print("Calculating mean and median biomasses for each functional group (2079-2100)...")
with alive_bar(4) as bar:
    mean_predictions_f, median_predictions_f = AnalyseGams.mean_and_median(
        predictions_cut_f, [], []
    )
    bar()
    t
    mean_predictions_rf, median_predictions_rf = AnalyseGams.mean_and_median(
        predictions_cut_rf, [], []
    )
    bar()
    t
    mean_darwin_f, median_darwin_f = AnalyseGams.mean_and_median(darwin_cut_f, [], [])

    Save.save_means_and_medians(
        ANALYSIS_SAVE,
        mean_predictions,
        median_predictions,
        mean_predictions_r,
        median_predictions_r,
        mean_darwin,
        median_darwin,
        mean_predictions_f,
        median_predictions_f,
        mean_predictions_rf,
        median_predictions_rf,
        mean_darwin_f,
        median_darwin_f,
    )
    bar()
    t

print(
    "Calculating ratios ((GAMs_[mean/med] - Darwin_[mean/med]) / Darwin_[mean/med]) (1987-2008)..."
)
with alive_bar(3) as bar:
    mean_ratios, median_ratios = AnalyseGams.calc_ratios(
        mean_predictions, mean_darwin, median_predictions, median_darwin, [], []
    )
    bar()
    t
    mean_ratios_r, median_ratios_r = AnalyseGams.calc_ratios(
        mean_predictions_r, mean_darwin, median_predictions_r, median_darwin, [], []
    )
    bar()
    t

print(
    "Calculating ratios ((GAMs_[mean/med] - Darwin_[mean/med]) / Darwin_[mean/med]) (2079-2100)..."
)
with alive_bar(3) as bar:
    mean_ratios_f, median_ratios_f = AnalyseGams.calc_ratios(
        mean_predictions_f, mean_darwin_f, median_predictions_f, median_darwin_f, [], []
    )
    bar()
    t
    mean_ratios_rf, median_ratios_rf = AnalyseGams.calc_ratios(
        mean_predictions_rf,
        mean_darwin_f,
        median_predictions_rf,
        median_darwin_f,
        [],
        [],
    )
    bar()
    t
    Save.save_ratios(
        ANALYSIS_SAVE,
        mean_ratios,
        median_ratios,
        mean_ratios_r,
        median_ratios_r,
        mean_ratios_f,
        median_ratios_f,
        mean_ratios_rf,
        median_ratios_rf,
    )
    bar()
    t

print("Calculating R^2 values...")
with alive_bar(2) as bar:
    rsq = AnalyseGams.r_squared(darwin_cut, predictions_cut)
    rsq_r = AnalyseGams.r_squared(darwin_cut_r, predictions_cut_r)
    bar()
    t
    rsq_f = AnalyseGams.r_squared(darwin_cut_f, predictions_cut_f)
    rsq_rf = AnalyseGams.r_squared(darwin_cut_rf, predictions_cut_rf)
    bar()
    t

    Save.save_rsq(ANALYSIS_SAVE, rsq, rsq_r, rsq_f, rsq_rf)


# print("Producing summary tables...")
# with alive_bar(4) as bar:
#     summary = AnalyseGams.summary_df(
#         cutoff_summary_p, means_p, meds_p, rsq_p, len(darwin_target_p["proko"])
#     )
#     summary_rand_p = AnalyseGams.summary_df(
#         cutoff_summary_rand_p,
#         means_rand_p,
#         meds_rand_p,
#         rsq_rand_p,
#         len(darwin_target_p["proko"]),
#     )
#     bar()
#     t
#     summary_f = AnalyseGams.summary_df(
#         cutoff_summary_f, means_f, meds_f, rsq_f, len(darwin_target_p["proko"])
#     )
#     summary_rand_f = AnalyseGams.summary_df(
#         cutoff_summary_rand_f,
#         means_rand_f,
#         meds_rand_f,
#         rsq_rand_f,
#         len(darwin_target_p["proko"]),
#     )
#     bar()
#     t
#     combined_df = AnalyseGams.combined_df(
#         [summary_p, summary_rand_p, summary_f, summary_rand_f]
#     )
#     combined_df.to_csv(f"{ANALYSIS_SAVE}/summary/summary_all.csv")
#     bar()
#     t
#     summary_p.to_pickle(f"{ANALYSIS_SAVE}/summary/summary_p.pkl")
#     summary_rand_p.to_pickle(f"{ANALYSIS_SAVE}/summary/summary_rand_p.pkl")
#     summary_f.to_pickle(f"{ANALYSIS_SAVE}/summary/summary_f.pkl")
#     summary_rand_f.to_pickle(f"{ANALYSIS_SAVE}/summary/summary_rand_f.pkl")
#     bar()
#     t
