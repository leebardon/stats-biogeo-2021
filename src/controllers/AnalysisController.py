import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import time
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.models.gams import AnalyseGams

base_path = Path(os.path.abspath(__file__)).parents[2]
GAMS_PRESENT = base_path / "results" / "gams_output" / "predictions_present"
GAMS_FUTURE = base_path / "results" / "gams_output" / "predictions_future"
DARWIN_TARGET = base_path / "data" / "processed" / "validation_sets" / "plankton"
ANALYSIS_SAVE = base_path / "results" / "analysis_output"


config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.05)


print("Getting GAMs predictions and Darwin target data...")
with alive_bar(3) as bar:
    with open(f"{GAMS_PRESENT}/predictions_p.pkl", "rb") as handle:
        gams_predictions_p = pickle.load(handle)
    with open(f"{GAMS_PRESENT}/predictions_random_p.pkl", "rb") as handle:
        gams_predictions_random_p = pickle.load(handle)
    bar()
    t
    with open(f"{GAMS_FUTURE}/predictions_f.pkl", "rb") as handle:
        gams_predictions_f = pickle.load(handle)
    with open(f"{GAMS_FUTURE}/predictions_random_f.pkl", "rb") as handle:
        gams_predictions_random_f = pickle.load(handle)
    bar()
    t
    with open(f"{DARWIN_TARGET}/plankton_ocean_present.pkl", "rb") as handle:
        darwin_target_p = pickle.load(handle)
    with open(f"{DARWIN_TARGET}/plankton_ocean_future.pkl", "rb") as handle:
        darwin_target_f = pickle.load(handle)
    bar()
    t

print(
    "Applying presence-absence cut-off, calculating false positives and negatives ..."
)
with alive_bar(5) as bar:
    gams_cut_p, darwin_cut_p, cutoff_summary_p = AnalyseGams.cut_off(
        gams_predictions_p, darwin_target_p, 1.001e-5
    )
    bar()
    t
    gams_cut_rand_p, darwin_cut_rand_p, cutoff_summary_rand_p = AnalyseGams.cut_off(
        gams_predictions_random_p, darwin_target_p, 1.001e-5
    )
    bar()
    t
    gams_cut_f, darwin_cut_f, cutoff_summary_f = AnalyseGams.cut_off(
        gams_predictions_f, darwin_target_f, 1.001e-5
    )
    bar()
    t
    gams_cut_rand_f, darwin_cut_rand_f, cutoff_summary_rand_f = AnalyseGams.cut_off(
        gams_predictions_random_f, darwin_target_f, 1.001e-5
    )
    bar()
    t
    AnalyseGams.save_with_cutoff_removed(
        ANALYSIS_SAVE,
        gams_cut_p,
        gams_cut_rand_p,
        darwin_cut_p,
        darwin_cut_rand_p,
        gams_cut_f,
        gams_cut_rand_f,
        darwin_cut_f,
        darwin_cut_rand_f,
        "cutoff/present",
        "cutoff/future",
    )
    bar()
    t

print("Calculating mean and median biomasses for each functional group (1987-2008)...")
with alive_bar(4) as bar:
    mean_gams_p, median_gams_p = AnalyseGams.mean_and_median(gams_cut_p, [], [])
    bar()
    t
    mean_gams_rand_p, median_gams_rand_p = AnalyseGams.mean_and_median(
        gams_rand_cut_p, [], []
    )
    bar()
    t
    mean_darwin_p, median_darwin_p = AnalyseGams.mean_and_median(darwin_cut_p, [], [])
    bar()
    t

print("Calculating mean and median biomasses for each functional group (2079-2100)...")
with alive_bar(4) as bar:
    mean_gams_f, median_gams_f = AnalyseGams.mean_and_median(gams_cut_f, [], [])
    bar()
    t
    mean_gams_rand_f, median_gams_rand_f = AnalyseGams.mean_and_median(
        gams_rand_cut_f, [], []
    )
    bar()
    t
    mean_darwin_f, median_darwin_f = AnalyseGams.mean_and_median(darwin_cut_f, [], [])

    AnalyseGams.save_means_and_medians(
        ANALYSIS_SAVE,
        mean_gams_p,
        median_gams_p,
        mean_gams_rand_p,
        median_gams_rand_p,
        mean_darwin_p,
        median_darwin_p,
        mean_gams_f,
        median_gams_f,
        mean_gams_rand_f,
        median_gams_rand_f,
        mean_darwin_f,
        median_darwin_f,
        "stats/present/means",
        "stats/present/medians",
        "stats/future/means",
        "stats/future/medians",
    )
    bar()
    t

print(
    "Calculating ratios ((GAMs_[mean/med] - Darwin_[mean/med]) / Darwin_[mean/med]) (1987-2008)..."
)
with alive_bar(3) as bar:
    mean_ratios_p, median_ratios_p = AnalyseGams.calc_ratios(
        mean_gams_p, mean_darwin_p, median_gams_p, median_darwin_p, [], []
    )
    bar()
    t
    mean_ratios_rand_p, median_ratios_rand_p = AnalyseGams.calc_ratios(
        mean_gams_rand_p, mean_darwin_p, median_gams_rand_p, median_darwin_p, [], []
    )
    bar()
    t

print(
    "Calculating ratios ((GAMs_[mean/med] - Darwin_[mean/med]) / Darwin_[mean/med]) (2079-2100)..."
)
with alive_bar(3) as bar:
    mean_ratios_f, median_ratios_f = AnalyseGams.calc_ratios(
        mean_gams_f, mean_darwin_f, median_gams_f, median_darwin_f, [], []
    )
    bar()
    t
    mean_ratios_rand_f, median_ratios_rand_f = AnalyseGams.calc_ratios(
        mean_gams_rand_f, mean_darwin_f, median_gams_rand_f, median_darwin_f, [], []
    )
    bar()
    t

    AnalyseGams.save_ratios(
        ANALYSIS_SAVE,
        mean_ratios_p,
        median_ratios_p,
        mean_ratios_rand_p,
        median_ratios_rand_p,
        mean_ratios_f,
        median_ratios_f,
        mean_ratios_rand_f,
        median_ratios_rand_f,
        "stats/present/ratios" "stats/future/ratios",
    )
    bar()
    t

print("Calculating R^2 values...")
with alive_bar(2) as bar:
    rsq_p = AnalyseGams.r_squared(darwin_cut_p, gams_cut_p)
    rsq_rand_p = AnalyseGams.r_squared(darwin_cut_rand_p, gams_cut_rand_p)
    bar()
    t
    rsq_f = AnalyseGams.r_squared(darwin_cut_f, gams_cut_f)
    rsq_rand_f = AnalyseGams.r_squared(darwin_cut_rand_f, gams_cut_rand_f)
    bar()
    t
    AnalyseGams.save_as_dict(ANALYSIS_SAVE, rsq_p, "stats/present/rsquared", "rsq_p")
    AnalyseGams.save_as_dict(
        ANALYSIS_SAVE, rsq_rand_p, "stats/present/rsquared", "rsq_rand_p"
    )
    AnalyseGams.save_as_dict(ANALYSIS_SAVE, rsq_f, "stats/future/rsquared", "rsq_f")
    AnalyseGams.save_as_dict(
        ANALYSIS_SAVE, rsq_rand_f, "stats/future/rsquared", "rsq_rand_f"
    )

print("Producing summary tables...")
with alive_bar(4) as bar:
    summary_p = AnalyseGams.summary_df(
        cutoff_summary_p, means_p, meds_p, rsq_p, len(darwin_target_p["proko"])
    )
    summary_rand_p = AnalyseGams.summary_df(
        cutoff_summary_rand_p,
        means_rand_p,
        meds_rand_p,
        rsq_rand_p,
        len(darwin_target_p["proko"]),
    )
    bar()
    t
    summary_f = AnalyseGams.summary_df(
        cutoff_summary_f, means_f, meds_f, rsq_f, len(darwin_target_p["proko"])
    )
    summary_rand_f = AnalyseGams.summary_df(
        cutoff_summary_rand_f,
        means_rand_f,
        meds_rand_f,
        rsq_rand_f,
        len(darwin_target_p["proko"]),
    )
    bar()
    t
    combined_df = AnalyseGams.combined_df(
        [summary_p, summary_rand_p, summary_f, summary_rand_f]
    )
    combined_df.to_csv(f"{ANALYSIS_SAVE}/summary/summary_all.csv")
    bar()
    t
    summary_p.to_pickle(f"{ANALYSIS_SAVE}/summary/summary_p.pkl")
    summary_rand_p.to_pickle(f"{ANALYSIS_SAVE}/summary/summary_rand_p.pkl")
    summary_f.to_pickle(f"{ANALYSIS_SAVE}/summary/summary_f.pkl")
    summary_rand_f.to_pickle(f"{ANALYSIS_SAVE}/summary/summary_rand_f.pkl")
    bar()
    t
