import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import time
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
t = time.sleep(2)


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
            "plankton_oce",
            "plankton_oce_f",
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
        cutoff_summary,
        cutoff_summary_r,
        cutoff_summary_f,
        cutoff_summary_rf,
    )
    bar()
    t

# print("Calculating mean and median biomasses for each functional group (1987-2008)...")
# with alive_bar(3) as bar:
#     mean_predictions, median_predictions = AnalyseGams.mean_and_median(predictions_cut)
#     bar()
#     time.sleep(30)  # to save fans on poor laptop...
#     mean_predictions_r, median_predictions_r = AnalyseGams.mean_and_median(
#         predictions_cut_r
#     )
#     bar()
#     t
#     time.sleep(30)
#     mean_darwin, median_darwin = AnalyseGams.mean_and_median(darwin_cut)
#     bar()
#     t
#     time.sleep(30)

# print("Calculating mean and median biomasses for each functional group (2079-2100)...")
# with alive_bar(3) as bar:
#     mean_predictions_f, median_predictions_f = AnalyseGams.mean_and_median(
#         predictions_cut_f
#     )
#     bar()
#     time.sleep(30)
#     mean_predictions_rf, median_predictions_rf = AnalyseGams.mean_and_median(
#         predictions_cut_rf
#     )
#     bar()
#     time.sleep(30)
#     mean_darwin_f, median_darwin_f = AnalyseGams.mean_and_median(darwin_cut_f)
#     bar()
#     time.sleep(30)

#     Save.save_means_and_medians(
#         ANALYSIS_SAVE,
#         mean_predictions,
#         median_predictions,
#         mean_predictions_r,
#         median_predictions_r,
#         mean_darwin,
#         median_darwin,
#         mean_predictions_f,
#         median_predictions_f,
#         mean_predictions_rf,
#         median_predictions_rf,
#         mean_darwin_f,
#         median_darwin_f,
#     )


# print(
#     "Calculating ratios ((GAMs_[mean/med] - Darwin_[mean/med]) / Darwin_[mean/med]) (1987-2008)..."
# )
# with alive_bar(2) as bar:
#     mean_ratios, median_ratios = AnalyseGams.calc_ratios(
#         mean_predictions, median_predictions, mean_darwin, median_darwin
#     )
#     bar()
#     t
#     mean_ratios_r, median_ratios_r = AnalyseGams.calc_ratios(
#         mean_predictions_r, median_predictions_r, mean_darwin, median_darwin
#     )
#     bar()
#     t

# print(
#     "Calculating ratios ((GAMs_[mean/med] - Darwin_[mean/med]) / Darwin_[mean/med]) (2079-2100)..."
# )
# with alive_bar(3) as bar:
#     mean_ratios_f, median_ratios_f = AnalyseGams.calc_ratios(
#         mean_predictions_f, median_predictions_f, mean_darwin_f, median_darwin_f
#     )
#     bar()
#     t
#     mean_ratios_rf, median_ratios_rf = AnalyseGams.calc_ratios(
#         mean_predictions_rf, median_predictions_rf, mean_darwin_f, median_darwin_f
#     )
#     bar()
#     t
#     Save.save_ratios(
#         ANALYSIS_SAVE,
#         mean_ratios,
#         median_ratios,
#         mean_ratios_r,
#         median_ratios_r,
#         mean_ratios_f,
#         median_ratios_f,
#         mean_ratios_rf,
#         median_ratios_rf,
#     )
#     bar()
#     t


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

thing = "/Users/leebardon/Dropbox/Development/stats_biogeo_2021/results/analysis_output/t_ratios/"
mean_ratios = pd.read_pickle(f"{thing}/present/mean_ratios.pkl")
median_ratios = pd.read_pickle(f"{thing}/present/median_ratios.pkl")
mean_ratios_r = pd.read_pickle(f"{thing}/present/mean_ratios_r.pkl")
median_ratios_r = pd.read_pickle(f"{thing}/present/median_ratios_r.pkl")
mean_ratios_f = pd.read_pickle(f"{thing}/future/mean_ratios_f.pkl")
median_ratios_f = pd.read_pickle(f"{thing}/future/median_ratios_f.pkl")
mean_ratios_rf = pd.read_pickle(f"{thing}/future/mean_ratios_rf.pkl")
median_ratios_rf = pd.read_pickle(f"{thing}/future/median_ratios_rf.pkl")


print("Producing summary tables...")
with alive_bar(3) as bar:
    summary_stats = AnalyseGams.return_summary(
        cutoff_summary, mean_ratios, median_ratios, rsq, len(darwin_ocean["Pro"])
    )
    summary_stats_r = AnalyseGams.return_summary(
        cutoff_summary_r,
        mean_ratios_r,
        median_ratios_r,
        rsq_r,
        len(darwin_ocean["Pro"]),
    )
    bar()
    t
    summary_stats_f = AnalyseGams.return_summary(
        cutoff_summary_f,
        mean_ratios_f,
        median_ratios_f,
        rsq_f,
        len(darwin_ocean["Pro"]),
    )
    summary_stats_rf = AnalyseGams.return_summary(
        cutoff_summary_rf,
        mean_ratios_rf,
        median_ratios_f,
        rsq_f,
        len(darwin_ocean["Pro"]),
    )
    bar()
    t

    combined_df = AnalyseGams.return_combined_df(
        [summary_stats, summary_stats_r, summary_stats_f, summary_stats_rf]
    )

    Save.save_summaries(
        ANALYSIS_SAVE,
        combined_df,
        summary_stats,
        summary_stats_r,
        summary_stats_f,
        summary_stats_rf,
    )
    bar()
    t
