import os
import sys
from time import sleep
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.models.gams import AnalyseGams
from src.models import Save

ROOT = Path(os.path.abspath(__file__)).parents[2]

# Load
PREDICTIONS = ROOT / "results" / "gams_output" / "predictions"
T_SETS = ROOT / "data" / "processed"
TARGETS = ROOT / "data" / "processed" / "validation_sets" / "plankton"
# Save
ANALYSIS_SAVE = Save.check_dir_exists(f"{ROOT}/results/analysis_output")


config_handler.set_global(length=50, spinner="fish_bouncing")


print("Getting GAMs predictions and Darwin target data...")
with alive_bar(2) as bar:
    try:
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
        sleep(2)
        (darwin_ocean, darwin_ocean_f,) = AnalyseGams.get_targets(
            f"{TARGETS}",
            *[
                "plankton_oce",
                "plankton_oce_f",
            ],
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem getting GAMs predictions or Darwin data ...")
        sys.exit(1)


print("Getting ecosystem sample sets to assess presence and absence...")
with alive_bar(1) as bar:
    try:
        (plank_ts, plank_ts_r,) = AnalyseGams.get_predictions(
            f"{T_SETS}/sampled_plankton",
            *[
                "plankton",
                "plankton_r",
            ],
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem getting ecosystem sample sets...")
        sys.exit(1)


print("Applying cutoff, calculating false pos, neg, sensitivity, specificity ...")
with alive_bar(5) as bar:
    try:
        gams_cut, darwin_cut, pres_abs_summary = AnalyseGams.pres_abs_summary(
            predictions, darwin_ocean
        )
        bar()
        sleep(2)
        gams_cut_r, darwin_cut_r, pres_abs_summary_r = AnalyseGams.pres_abs_summary(
            predictions_r, darwin_ocean
        )
        bar()
        sleep(2)
        gams_cut_f, darwin_cut_f, pres_abs_summary_f = AnalyseGams.pres_abs_summary(
            predictions_f, darwin_ocean_f
        )
        bar()
        sleep(2)
        gams_cut_rf, darwin_cut_rf, pres_abs_summary_rf = AnalyseGams.pres_abs_summary(
            predictions_rf, darwin_ocean_f
        )
        bar()
        sleep(2)
        Save.save_pres_abs_summary(
            ANALYSIS_SAVE,
            pres_abs_summary,
            pres_abs_summary_r,
            pres_abs_summary_f,
            pres_abs_summary_rf,
        )
        Save.save_falsepos_falseneg()
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem applying cutoff, false pos, neg, sens., spec....")
        sys.exit(1)


print("Assessing presence-absence balance in training sets...")
with alive_bar(1) as bar:
    try:
        ts_balance = AnalyseGams.pres_abs_tsets(plank_ts)
        ts_balance_r = AnalyseGams.pres_abs_tsets(plank_ts_r)
        bar()
        sleep(2)

    except:
        print(
            " \n ERROR: Problem assessing presence-absence balance in training sets...."
        )
        sys.exit(1)


print("Calculating mean and median biomasses for each functional group (1987-2008)...")
with alive_bar(3) as bar:
    try:
        mean_gams, median_gams = AnalyseGams.mean_and_median(gams_cut)
        bar()
        sleep(15)
        mean_gams_r, median_gams_r = AnalyseGams.mean_and_median(gams_cut_r)
        bar()
        sleep(15)
        mean_darwin, median_darwin = AnalyseGams.mean_and_median(darwin_cut)
        bar()
        sleep(15)

    except:
        print(" \n ERROR: Problem calc. mean and median biomasses (1987-2008)....")
        sys.exit(1)


print("Calculating mean and median biomasses for each functional group (2079-2100)...")
with alive_bar(3) as bar:
    try:
        mean_gams_f, median_gams_f = AnalyseGams.mean_and_median(gams_cut_f)
        bar()
        sleep(15)
        mean_gams_rf, median_gams_rf = AnalyseGams.mean_and_median(gams_cut_rf)
        bar()
        sleep(15)
        mean_darwin_f, median_darwin_f = AnalyseGams.mean_and_median(darwin_cut_f)
        bar()
        sleep(15)
        Save.save_means_and_medians(
            ANALYSIS_SAVE,
            mean_gams,
            median_gams,
            mean_gams_r,
            median_gams_r,
            mean_darwin,
            median_darwin,
            mean_gams_f,
            median_gams_f,
            mean_gams_rf,
            median_gams_rf,
            mean_darwin_f,
            median_darwin_f,
        )

    except:
        print(" \n ERROR: Problem calc. mean and median biomasses (2079-2100)....")
        sys.exit(1)


print("Calculating biases (mean and median ratios) (1987-2008)...")
with alive_bar(2) as bar:
    try:
        mean_ratios, median_ratios = AnalyseGams.calc_ratios(
            mean_gams, median_gams, mean_darwin, median_darwin
        )
        bar()
        sleep(2)
        mean_ratios_r, median_ratios_r = AnalyseGams.calc_ratios(
            mean_gams_r, median_gams_r, mean_darwin, median_darwin
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem calc. biases (1987-2008)....")
        sys.exit(1)


print("Calculating biases (mean and median ratios) (2079-2100)...")
with alive_bar(3) as bar:
    try:
        mean_ratios_f, median_ratios_f = AnalyseGams.calc_ratios(
            mean_gams_f, median_gams_f, mean_darwin_f, median_darwin_f
        )
        bar()
        sleep(2)
        mean_ratios_rf, median_ratios_rf = AnalyseGams.calc_ratios(
            mean_gams_rf, median_gams_rf, mean_darwin_f, median_darwin_f
        )
        bar()
        sleep(2)
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
        sleep(2)

    except:
        print(" \n ERROR: Problem calc. biases (2079-2100)....")
        sys.exit(1)


print("Calculating R^2 values...")
with alive_bar(2) as bar:
    try:
        rsq = AnalyseGams.r_squared(darwin_cut, gams_cut)
        rsq_r = AnalyseGams.r_squared(darwin_cut_r, gams_cut_r)
        bar()
        sleep(2)
        rsq_f = AnalyseGams.r_squared(darwin_cut_f, gams_cut_f)
        rsq_rf = AnalyseGams.r_squared(darwin_cut_rf, gams_cut_rf)
        bar()
        sleep(2)
        Save.save_rsq(ANALYSIS_SAVE, rsq, rsq_r, rsq_f, rsq_rf)

    except:
        print(" \n ERROR: Problem calc. r-squared ....")
        sys.exit(1)


print("Producing summary tables...")
with alive_bar(3) as bar:
    try:
        summary_stats = AnalyseGams.return_summary(
            pres_abs_summary, mean_ratios, median_ratios, rsq, len(darwin_ocean["Pro"])
        )
        summary_stats_r = AnalyseGams.return_summary(
            pres_abs_summary_r,
            mean_ratios_r,
            median_ratios_r,
            rsq_r,
            len(darwin_ocean["Pro"]),
        )
        bar()
        sleep(2)
        summary_stats_f = AnalyseGams.return_summary(
            pres_abs_summary_f,
            mean_ratios_f,
            median_ratios_f,
            rsq_f,
            len(darwin_ocean["Pro"]),
        )
        summary_stats_rf = AnalyseGams.return_summary(
            pres_abs_summary_rf,
            mean_ratios_rf,
            median_ratios_rf,
            rsq_rf,
            len(darwin_ocean["Pro"]),
        )
        bar()
        sleep(2)
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
        sleep(2)

    except:
        print(" \n ERROR: Problem producing summary csv files....")
        sys.exit(1)

    sys.exit(1)
