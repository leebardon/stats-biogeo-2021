import time
import os
import numpy as np
import pandas as pd
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.models import Save, SaveST
from src.models.build_training_sets import TrainingSetBuilder as TSB
from src.models.sample_size_testing import (
    SizeTestMatrices,
    SizeTestSampling,
    SizeTestGams,
)

ROOT = Path(os.path.abspath(__file__)).parents[2]
INTERIM = ROOT / "data" / "interim"
PROC = ROOT / "data" / "processed"
DARWIN = ROOT / "results" / "analysis_output" / "stats" / "mean_med"
SIZE_TESTS = Save.check_dir_exists(f"{PROC}/size_tests")
CUTOFF = 1.001e-5

config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(2)
TEST_MATRIX_SEEDS = [np.arange(19)]


#
# print("Generating 18 random sampling matrices from (N=100 .. N=18,000)...")
# with alive_bar(1) as bar:
#     matrices, num_cells = SizeTestMatrices.random_test_matrices(TEST_MATRIX_SEEDS)
#     SaveST.size_test_matrices(INTERIM, matrices, num_cells)
#     bar()
#     t


# print("Obtaining Darwin ecosystem and physical data...")
# with alive_bar(1) as bar:
#     ecosys = pd.read_pickle(f"{PROC}/model_ocean_data/present/ecosys_ocean_p.pkl")
#     sss, sst, par = TSB.get_data(
#         f"{PROC}/model_ocean_data/present",
#         *[
#             "sss_ocean_p.pkl",
#             "sst_ocean_p.pkl",
#             "par_ocean.pkl",
#         ],
#     )
#     bar()
#     t

# print("Merging randomly-sampled test matrices with ecosystem data...")
# with alive_bar(2) as bar:
#     reshaped = SizeTestSampling.reshape_test_matrices(matrices)
#     dataframes = SizeTestSampling.return_test_dataframes(reshaped)
#     bar()
#     t
#     merged = SizeTestSampling.merge_test_matrices_and_ecosys_data(dataframes, ecosys)
#     sampled_ecosys_dfs = SizeTestSampling.check_land_removed(merged)
#     SaveST.size_test_sampled_ecosys(INTERIM, sampled_ecosys_dfs)
#     bar()
#     t

# print("Building plankton and predictor training sets for sample size tests...")
# with alive_bar(1) as bar:
#     predictor_tsets = SizeTestGams.build_predictor_tsets(
#         sampled_ecosys_dfs, sss, sst, par
#     )
#     cocco_tsets, diatom_tsets = SizeTestGams.build_plankton_tsets(sampled_ecosys_dfs)
#
#     SaveST.size_test_training_sets(SIZE_TESTS, predictor_tsets, cocco_tsets, diatom_tsets)
#     bar()
#     t


# print("Fitting GAMs to test samples...")
# with alive_bar(2) as bar:
#     cocco_cut, diatom_cut = SizeTestGams.apply_size_test_cutoff(
#         CUTOFF, cocco_tsets, diatom_tsets
#     )
#     bar()
#     t
#     cocco_gams, diatom_gams = SizeTestGams.fit_size_test_gams(
#         cocco_cut, diatom_cut, predictor_tsets
#     )
#     bar()
#     t


# print("Making predictions (1987-2008)...")
# with alive_bar(2) as bar:
#     predictors_oce = f"{PROC}/validation_sets/predictors/predictors_oce.pkl"
#     cocco_predictions = SizeTestGams.make_size_test_predictions("coccos", cocco_gams, predictors_oce)
#     bar()
#     time.sleep(60)
#     diatom_predictions = SizeTestGams.make_size_test_predictions("diatoms", diatom_gams, predictors_oce)
#     bar()
#     t

# print("Making predictions (2079-2100)...")
# with alive_bar(3) as bar:
#     predictors_oce_f = f"{PROC}/validation_sets/predictors/predictors_oce_f.pkl"
#     cocco_predictions_f = SizeTestGams.make_size_test_predictions(
#         "coccos_f", cocco_gams, predictors_oce_f
#     )
#     bar()
#     time.sleep(60)
#     diatom_predictions_f = SizeTestGams.make_size_test_predictions(
#         "diatoms_f", diatom_gams, predictors_oce_f
#     )
#     bar()
#     t
#     SaveST.save_predictions(
#         Save.check_dir_exists(f"{SIZE_TESTS}/predictions"),
#         **{
#             "cocco_predictions": cocco_predictions,
#             "diatom_predictions": diatom_predictions,
            # "cocco_predictions_f": cocco_predictions_f,
            # "diatom_predictions_f": diatom_predictions_f,
        # },
    # )
#     bar()
#     t


from src.models.gams import AnalyseGams
(
    diatom_predictions,
    cocco_predictions,
    diatom_predictions_f,
    cocco_predictions_f,
) = AnalyseGams.get_predictions(
    f"{SIZE_TESTS}/predictions",
    *[
        "diatom_predictions",
        "cocco_predictions",
        "diatom_predictions_f",
        "cocco_predictions_f",
    ],
)

print("Applying cutoff, calculating false pos, neg, sensitivity, specificity ...")
with alive_bar(2) as bar:
    (darwin, darwin_f,) = AnalyseGams.get_targets(
        f"{PROC}/validation_sets/plankton/",
        *[
            "plankton_oce",
            "plankton_oce_f",
        ],
    )
    bar()
    t
    cocco_cut, darwin_cut, cocco_summary = AnalyseGams.pres_abs_summary(
        cocco_predictions, darwin
    )
    diatom_cut, darwin_cut, diatom_summary = AnalyseGams.pres_abs_summary(
        diatom_predictions, darwin
    )
    bar()
    t
    cocco_cut_f, darwin_cut_f, cocco_summary_f = AnalyseGams.pres_abs_summary(
        cocco_predictions_f, darwin_f
    )
    diatom_cut_f, darwin_cut_f, diatom_summary_f = AnalyseGams.pres_abs_summary(
        diatom_predictions_f, darwin_f
    )

    Save.save_size_test_summaries(
        SIZE_TESTS,
        cocco_summary,
        diatom_summary,
        cocco_summary_f,
        diatom_summary_f,
    )
    bar()
    t


print("Calculating mean and median size test biomasses (1987-2008)...")
with alive_bar(2) as bar:
    mean_cocco, median_cocco = AnalyseGams.mean_and_median(cocco_cut)
    bar()
    time.sleep(15)
    mean_diatom, median_diatom = AnalyseGams.mean_and_median(diatom_cut)
    bar()
    time.sleep(15)


print("Calculating mean and median size test biomasses (2079-2100)...")
with alive_bar(2) as bar:
    mean_cocco_f, median_cocco_f = AnalyseGams.mean_and_median(cocco_cut_f)
    bar()
    time.sleep(15)
    mean_diatom_f, median_diatom_f = AnalyseGams.mean_and_median(diatom_cut_f)
    bar()
    time.sleep(15)

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


print(
    "Calc. mean and median ratios (1987-2008)..."
)
with alive_bar(2) as bar:
    (mean_darwin, median_darwin, mean_darwin_f, median_darwin_f) = SizeTestGams.get_darwin_stats(
        DARWIN,
        *[
            "mean_darwin",
            "median_darwin",
            "mean_darwin_f",
            "median_darwin_f",
        ],
    )
    cocco_mean_ratios, cocco_median_ratios = AnalyseGams.calc_ratios(
        mean_cocco, median_cocco, mean_darwin, median_darwin
    )
    bar()
    t
    diatom_mean_ratios, diatom_median_ratios = AnalyseGams.calc_ratios(
        mean_diatom, median_diatom, mean_darwin, median_darwin
    )
    bar()
    t

print(
    "Calc. mean and median ratios (2079-2100)..."
)
with alive_bar(3) as bar:
    cocco_mean_ratios_f, cocco_median_ratios_f = AnalyseGams.calc_ratios(
        mean_cocco_f, median_cocco_f, mean_darwin_f, median_darwin_f
    )
    bar()
    t
    diatom_mean_ratios_f, diatom_median_ratios_f = AnalyseGams.calc_ratios(
        mean_diatom_f, median_diatom_f, mean_darwin_f, median_darwin_f
    )
    bar()
    t
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
    t


print("Calculating R^2 values...")
with alive_bar(2) as bar:
    cocco_rsq = AnalyseGams.r_squared(darwin_cut, cocco_cut)
    diatom_rsq = AnalyseGams.r_squared(darwin_cut, diatom_cut)
    bar()
    t
    cocco_rsq_f = AnalyseGams.r_squared(darwin_cut_f, cocco_cut_f)
    diatom_rsq_f = AnalyseGams.r_squared(darwin_cut_f, diatom_cut_f)
    bar()
    t
    SaveST.save_rsq(SIZE_TESTS, cocco_rsq, diatom_rsq, cocco_rsq_f, diatom_rsq_f)


print("Producing summary tables...")
with alive_bar(5) as bar:
    cocco_summary_stats = AnalyseGams.return_summary(
        cocco_summary, cocco_mean_ratios, cocco_median_ratios, cocco_rsq, len(darwin["Pro"])
    )
    bar()
    t
    diatom_summary_stats = AnalyseGams.return_summary(
        diatom_summary, diatom_mean_ratios, diatom_median_ratios, diatom_rsq, len(darwin["Pro"])
    )
    bar()
    t
    cocco_summary_stats_f = AnalyseGams.return_summary(
        cocco_summary_f, cocco_mean_ratios_f, cocco_median_ratios_f, cocco_rsq_f, len(darwin["Pro"])
    )
    bar()
    t
    diatom_summary_stats_f = AnalyseGams.return_summary(
        diatom_summary_f, diatom_mean_ratios_f, diatom_median_ratios_f, diatom_rsq_f, len(darwin["Pro"])
    )
    bar()
    t
    combined_df = AnalyseGams.return_combined_df(
        [cocco_summary_stats, diatom_summary_stats, cocco_summary_stats_f, diatom_summary_stats_f]
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
    t

