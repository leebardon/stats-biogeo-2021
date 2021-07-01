import os
import sys
import numpy as np
import pandas as pd
from time import sleep
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.models import Save, SaveST
from src.models.gams import AnalyseGams
from src.models.build_training_sets import TrainingSetBuilder as TSB
from src.models.sample_size_testing import (
    SizeTestMatrices,
    SizeTestSampling,
    SizeTestGams,
    SizeTestAnalysis,
)

ROOT = Path(os.path.abspath(__file__)).parents[2]
# Load
INTERIM = ROOT / "data" / "interim"
PROC = ROOT / "data" / "processed"
# Save
DARWIN = ROOT / "results" / "analysis_output" / "stats" / "mean_med"
SIZE_TESTS = Save.check_dir_exists(f"{PROC}/size_tests")
CUTOFF = 1.001e-5


config_handler.set_global(length=50, spinner="fish_bouncing")
TEST_MATRIX_SEEDS = [np.arange(19)]


print("Generating 18 random sampling matrices from (N=100 .. N=18,000)...")
with alive_bar(1) as bar:
    try:
        matrices, num_cells = SizeTestMatrices.random_test_matrices(TEST_MATRIX_SEEDS)
        SaveST.size_test_matrices(INTERIM, matrices, num_cells)
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem seeding random matrices...")
        sys.exit(1)


print("Obtaining Darwin ecosystem and physical data...")
with alive_bar(1) as bar:
    try:
        ecosys = pd.read_pickle(f"{PROC}/model_ocean_data/present/ecosys_ocean_p.pkl")
        sss, sst, par = TSB.get_data(
            f"{PROC}/model_ocean_data/present",
            *[
                "sss_ocean_p.pkl",
                "sst_ocean_p.pkl",
                "par_ocean.pkl",
            ],
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem retrieving ecosys and physical data...")
        sys.exit(1)


print("Merging randomly-sampled test matrices with ecosystem data...")
with alive_bar(2) as bar:
    try:
        reshaped = SizeTestSampling.reshape_test_matrices(matrices)
        dataframes = SizeTestSampling.return_test_dataframes(reshaped)
        bar()
        sleep(2)
        merged = SizeTestSampling.merge_test_matrices_and_ecosys_data(
            dataframes, ecosys
        )
        sampled_ecosys_dfs = SizeTestSampling.check_land_removed(merged)
        SaveST.size_test_sampled_ecosys(INTERIM, sampled_ecosys_dfs)
        CELLS = [len(df) for df in sampled_ecosys_dfs]
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem merging matrices with ecosystem data ...")
        sys.exit(1)


print("Building plankton and predictor training sets for sample size tests...")
with alive_bar(1) as bar:
    try:
        predictor_tsets = SizeTestGams.build_predictor_tsets(
            sampled_ecosys_dfs, sss, sst, par
        )
        cocco_tsets, diatom_tsets = SizeTestGams.build_plankton_tsets(
            sampled_ecosys_dfs
        )

        SaveST.size_test_training_sets(
            SIZE_TESTS, predictor_tsets, cocco_tsets, diatom_tsets
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem plankton and predictor training sets ...")
        sys.exit(1)


print("Fitting GAMs to test samples...")
with alive_bar(2) as bar:
    try:
        cocco_cut, diatom_cut = SizeTestGams.apply_size_test_cutoff(
            CUTOFF, cocco_tsets, diatom_tsets
        )
        bar()
        sleep(2)
        cocco_gams, diatom_gams = SizeTestGams.fit_size_test_gams(
            cocco_cut, diatom_cut, predictor_tsets
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem fitting GAMs ...")
        sys.exit(1)


print("Making predictions (1987-2008)...")
with alive_bar(2) as bar:
    try:
        predictors_oce = f"{PROC}/validation_sets/predictors/predictors_oce.pkl"
        cocco_predictions = SizeTestGams.make_size_test_predictions(
            "coccos", cocco_gams, predictors_oce
        )
        bar()
        sleep(60)
        diatom_predictions = SizeTestGams.make_size_test_predictions(
            "diatoms", diatom_gams, predictors_oce
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem making predictions (1987-2008) ...")
        sys.exit(1)


print("Making predictions (2079-2100)...")
with alive_bar(3) as bar:
    try:
        predictors_oce_f = f"{PROC}/validation_sets/predictors/predictors_oce_f.pkl"
        cocco_predictions_f = SizeTestGams.make_size_test_predictions(
            "coccos_f", cocco_gams, predictors_oce_f
        )
        bar()
        sleep(60)
        diatom_predictions_f = SizeTestGams.make_size_test_predictions(
            "diatoms_f", diatom_gams, predictors_oce_f
        )
        bar()
        sleep(2)
        SaveST.save_predictions(
            Save.check_dir_exists(f"{SIZE_TESTS}/predictions"),
            **{
                "cocco_predictions": cocco_predictions,
                "diatom_predictions": diatom_predictions,
                "cocco_predictions_f": cocco_predictions_f,
                "diatom_predictions_f": diatom_predictions_f,
            },
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem making predictions (2079-2100) ...")
        sys.exit(1)


print("Applying cutoff, calculating false pos, neg, sensitivity, specificity ...")
with alive_bar(3) as bar:
    try:
        (darwin, darwin_f,) = AnalyseGams.get_targets(
            f"{PROC}/validation_sets/plankton/",
            *[
                "plankton_oce",
                "plankton_oce_f",
            ],
        )
        bar()
        sleep(2)
        cocco_cut, darwin_cocco_cut, cocco_summary = SizeTestAnalysis.pres_abs_summary(
            cocco_predictions,
            darwin,
            CELLS,
            "cocco",
        )
        (
            diatom_cut,
            darwin_diatom_cut,
            diatom_summary,
        ) = SizeTestAnalysis.pres_abs_summary(
            diatom_predictions,
            darwin,
            CELLS,
            "diatom",
        )
        bar()
        sleep(2)
        (
            cocco_cut_f,
            darwin_cocco_cut_f,
            cocco_summary_f,
        ) = SizeTestAnalysis.pres_abs_summary(
            cocco_predictions_f,
            darwin_f,
            CELLS,
            "cocco",
            "_f",
        )
        (
            diatom_cut_f,
            darwin_diatom_cut_f,
            diatom_summary_f,
        ) = SizeTestAnalysis.pres_abs_summary(
            diatom_predictions_f,
            darwin_f,
            CELLS,
            "diatom",
            "_f",
        )
        SaveST.save_pres_abs_summary(
            SIZE_TESTS,
            cocco_summary,
            diatom_summary,
            cocco_summary_f,
            diatom_summary_f,
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem w/ cutoff, false pos, neg, sens., spec. ...")
        sys.exit(1)


print("Calculating mean and median size test biomasses (1987-2008)...")
with alive_bar(2) as bar:
    try:
        mean_cocco, median_cocco = AnalyseGams.mean_and_median(cocco_cut)
        bar()
        sleep(15)
        mean_diatom, median_diatom = AnalyseGams.mean_and_median(diatom_cut)
        bar()
        sleep(15)

    except:
        print(
            " \n ERROR: Problem w/ mean and median size test biomasses (1987-2008)..."
        )
        sys.exit(1)


print("Calculating mean and median size test biomasses (2079-2100)...")
with alive_bar(2) as bar:
    try:
        mean_cocco_f, median_cocco_f = AnalyseGams.mean_and_median(cocco_cut_f)
        bar()
        sleep(15)
        mean_diatom_f, median_diatom_f = AnalyseGams.mean_and_median(diatom_cut_f)
        bar()
        sleep(15)

        SaveST.save_means_and_medians(
            SIZE_TESTS,
            mean_cocco,
            median_cocco,
            mean_diatom,
            median_diatom,
            mean_cocco_f,
            median_cocco_f,
            mean_diatom_f,
            median_diatom_f,
        )

    except:
        print(
            " \n ERROR: Problem w/ mean and median size test biomasses (2079-2100)..."
        )
        sys.exit(1)


print("Calc. mean and median ratios (1987-2008)...")
with alive_bar(2) as bar:
    try:
        (
            mean_darwin,
            median_darwin,
            mean_darwin_f,
            median_darwin_f,
        ) = SizeTestGams.get_darwin_stats(
            DARWIN,
            *[
                "mean_darwin",
                "median_darwin",
                "mean_darwin_f",
                "median_darwin_f",
            ],
        )
        cocco_mean_ratios, cocco_median_ratios = SizeTestAnalysis.calc_ratios(
            mean_cocco, median_cocco, mean_darwin[2], median_darwin[2]
        )
        bar()
        sleep(2)
        diatom_mean_ratios, diatom_median_ratios = SizeTestAnalysis.calc_ratios(
            mean_diatom, median_diatom, mean_darwin[4], median_darwin[4]
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem calc. mean and median ratios (1987-2008)...")
        sys.exit(1)


print("Calc. mean and median ratios (2079-2100)...")
with alive_bar(3) as bar:
    try:
        cocco_mean_ratios_f, cocco_median_ratios_f = SizeTestAnalysis.calc_ratios(
            mean_cocco_f, median_cocco_f, mean_darwin_f[2], median_darwin_f[2]
        )
        bar()
        sleep(2)
        diatom_mean_ratios_f, diatom_median_ratios_f = SizeTestAnalysis.calc_ratios(
            mean_diatom_f, median_diatom_f, mean_darwin_f[4], median_darwin_f[4]
        )
        bar()
        sleep(2)
        SaveST.save_ratios(
            SIZE_TESTS,
            cocco_mean_ratios,
            cocco_median_ratios,
            diatom_mean_ratios,
            diatom_median_ratios,
            cocco_mean_ratios_f,
            cocco_median_ratios_f,
            diatom_mean_ratios_f,
            diatom_median_ratios_f,
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem calc. mean and median ratios (2079-2100)...")
        sys.exit(1)


print("Calculating R^2 values...")
with alive_bar(2) as bar:
    try:
        cocco_rsq = AnalyseGams.r_squared(darwin_cocco_cut, cocco_cut)
        diatom_rsq = AnalyseGams.r_squared(darwin_diatom_cut, diatom_cut)
        bar()
        sleep(2)
        cocco_rsq_f = AnalyseGams.r_squared(darwin_cocco_cut_f, cocco_cut_f)
        diatom_rsq_f = AnalyseGams.r_squared(darwin_diatom_cut_f, diatom_cut_f)
        bar()
        sleep(2)
        SaveST.save_rsq(SIZE_TESTS, cocco_rsq, diatom_rsq, cocco_rsq_f, diatom_rsq_f)

    except:
        print(" \n ERROR: Problem calc. r-squared values...")
        sys.exit(1)


print("Producing summary tables...")
with alive_bar(5) as bar:
    try:
        cocco_summary_stats = SizeTestAnalysis.return_summary(
            cocco_summary,
            cocco_mean_ratios,
            cocco_median_ratios,
            cocco_rsq,
        )
        bar()
        sleep(2)
        diatom_summary_stats = SizeTestAnalysis.return_summary(
            diatom_summary,
            diatom_mean_ratios,
            diatom_median_ratios,
            diatom_rsq,
        )
        bar()
        sleep(2)
        cocco_summary_stats_f = SizeTestAnalysis.return_summary(
            cocco_summary_f,
            cocco_mean_ratios_f,
            cocco_median_ratios_f,
            cocco_rsq_f,
        )
        bar()
        sleep(2)
        diatom_summary_stats_f = SizeTestAnalysis.return_summary(
            diatom_summary_f,
            diatom_mean_ratios_f,
            diatom_median_ratios_f,
            diatom_rsq_f,
        )
        bar()
        sleep(2)
        combined_df = SizeTestAnalysis.return_combined_df(
            [
                cocco_summary_stats,
                diatom_summary_stats,
                cocco_summary_stats_f,
                diatom_summary_stats_f,
            ]
        )
        SaveST.save_summaries(
            SIZE_TESTS,
            combined_df,
            cocco_summary_stats,
            diatom_summary_stats,
            cocco_summary_stats_f,
            diatom_summary_stats_f,
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem producing summary csv files...")
        sys.exit(1)

    sys.exit(1)
