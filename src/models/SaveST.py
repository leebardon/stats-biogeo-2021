import os
import pickle
import numpy as np
import pandas as pd

from src.models import Save

def size_test_matrices(path, test_matrices, num_cells):
    BASE = check_dir_exists(f"{path}/size_tests")
    out = check_dir_exists(f"{BASE}/matrices")
    for i, M in enumerate(test_matrices):
        np.save(
            f"{out}/M{num_cells[i]}",
            M,
            allow_pickle=True,
        )


def size_test_sampled_ecosys(path, sampled_ecosys_dfs):
    BASE = Save.check_dir_exists(f"{path}/size_tests")
    out = Save.check_dir_exists(f"{BASE}/sampled_ecosys")
    for df in sampled_ecosys_dfs:
        df.to_pickle(f"{out}/sampled_{len(df)}.pkl")


def size_test_training_sets(path, predictor_tsets, cocco_tsets, diatom_tsets):
    TS = Save.check_dir_exists(f"{path}/training_sets")
    PRED = Save.check_dir_exists(f"{TS}/predictors")
    PLANK = Save.check_dir_exists(f"{TS}/plankton")
    save_test_tsets(PRED, "pred_tset", predictor_tsets)
    save_test_tsets(PLANK, "cocco_tset", cocco_tsets)
    save_test_tsets(PLANK, "diatom_tset", diatom_tsets)


def save_test_tsets(path, type, tsets):
    for tset in tsets:
        tset.to_pickle(f"{path}/{type}_{len(tset)}.pkl")


def save_size_test_predictions(path, predictions_dict):
    filepath = Save.check_dir_exists(f"{path}/predictions")
    for test_name, predictions in predictions_dict.items():
        predictions.to_pickle(f"{filepath}/{test_name}.pkl")


def save_pres_abs_summary(
    basepath,
    cocco_summary,
    diatom_summary,
    cocco_summary_f,
    diatom_summary_f,
):
    subdir = Save.check_dir_exists(f"{basepath}/presence_absence")
    Save.check_dir_exists(f"{subdir}/summaries")
    Save.save_stats(
        f"{subdir}",
        "summaries",
        **{
            "cocco_summary": cocco_summary,
            "diatom_summary": diatom_summary,
            "cocco_summary_f": cocco_summary_f,
            "diatom_summary_f": diatom_summary_f,
        },
    )


def save_means_and_medians(
    basepath,
    mean_cocco,
    median_cocco,
    mean_diatom,
    median_diatom,
    mean_cocco_f,
    median_cocco_f,
    mean_diatom_f,
    median_diatom_f,
):
    statsDir = Save.check_dir_exists(f"{basepath}/stats")
    subdir = Save.check_dir_exists(f"{statsDir}/mean_med")
    Save.check_dir_exists(f"{subdir}/present")
    Save.check_dir_exists(f"{subdir}/future")
    Save.save_stats(
        f"{subdir}",
        "present",
        **{
            "mean_cocco": mean_cocco,
            "median_cocco": median_cocco,
            "mean_diatoms": mean_diatom,
            "median_diatoms": median_diatom,
        },
    )
    Save.save_stats(
        f"{subdir}",
        "future",
        **{
            "mean_cocco_f": mean_cocco_f,
            "median_cocco_f": median_cocco_f,
            "mean_diatoms_f": mean_diatom_f,
            "median_diatoms_f": median_diatom_f,
        },
    )

def save_ratios(
    basepath,
    cocco_mean_ratios,
    cocco_median_ratios,
    diatom_mean_ratios,
    diatom_median_ratios,
    cocco_mean_ratios_f,
    cocco_median_ratios_f,
    diatom_mean_ratios_f,
    diatom_median_ratios_f,
):
    statsDir = Save.check_dir_exists(f"{basepath}/stats")
    subdir = Save.check_dir_exists(f"{statsDir}/ratios")
    Save.check_dir_exists(f"{subdir}/present")
    Save.check_dir_exists(f"{subdir}/future")
    Save.save_stats(
        f"{subdir}",
        "present",
        **{
            "cocco_mean_ratios": cocco_mean_ratios,
            "cocco_median_ratios": cocco_median_ratios,
            "diatoms_mean_ratios": diatom_mean_ratios,
            "diatoms_median_ratios": diatom_median_ratios,
        },
    )
    Save.save_stats(
        f"{subdir}",
        "future",
        **{
            "cocco_mean_ratios_f": cocco_mean_ratios_f,
            "cocco_median_ratios_f": cocco_median_ratios_f,
            "diatoms_mean_ratios_f": diatom_mean_ratios_f,
            "diatoms_median_ratios_f": diatom_median_ratios_f,
        },
    )

def save_rsq(
    basepath,
    cocco_rsq,
    diatom_rsq,
    cocco_rsq_f,
    diatom_rsq_f
):
    statsDir = Save.check_dir_exists(f"{basepath}/stats")
    subdir = Save.check_dir_exists(f"{statsDir}/rsquared")
    Save.check_dir_exists(f"{subdir}/present")
    Save.check_dir_exists(f"{subdir}/future")
    Save.save_stats(
        f"{subdir}",
        "present",
        **{
            "cocco_rsq": cocco_rsq,
            "diatom_rsq": diatom_rsq,
        },
    )
    Save.save_stats(
        f"{subdir}",
        "future",
        **{
            "cocco_rsq_f": cocco_rsq_f,
            "diatom_rsq_f": diatom_rsq_f,
        },
    )

def save_summaries(
        basepath,
        combined_df,
        cocco_summary_stats,
        diatom_summary_stats,
        cocco_summary_stats_f,
        diatom_summary_stats_f,
):
    subdir = Save.check_dir_exists(f"{basepath}/summary")
    combined_df.to_csv(f"{subdir}/summary_sizetests.csv")
    Save.save_stats(
        f"{basepath}",
        "summary",
        **{
            "cocco_summary": cocco_summary_stats,
            "diatom_summary": diatom_summary_stats,
            "cocco_summary_f": cocco_summary_stats_f,
            "diatom_summary_f": diatom_summary_stats_f,
        },
    )