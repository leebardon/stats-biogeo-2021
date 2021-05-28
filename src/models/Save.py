import os
import pickle
import numpy as np

# ADD SOMETHING TO SAVE OUTPUT FILE DETAILING E.G. SHAPE, MIN AND MAX X/Y


def check_dir_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def save_to_pkl(path, **kwargs):
    check_dir_exists(path)
    for filename, df in kwargs.items():
        df.to_pickle(f"{path}/{filename}")


def save_matrix(path, **matrices):
    check_dir_exists(path)
    for filename, matrix in matrices.items():
        np.save(
            f"{path}/{filename}",
            matrix,
            allow_pickle=True,
        )


def plankton_dicts(path, **dictionary_sets):
    for filename, data in dictionary_sets.items():
        plankton = {
            "Pro": data[0],
            "Pico": data[1],
            "Cocco": data[2],
            "Diazo": data[3],
            "Diatom": data[4],
            "Dino": data[5],
            "Zoo": data[6],
        }
        with open(f"{path}/{filename}.pkl", "wb") as handle:
            pickle.dump(plankton, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save_gams(path, **gams_sets):
    check_dir_exists(path)
    for group, gam in gams_sets.items():
        with open(f"{path}/{group}.pkl", "wb") as handle:
            pickle.dump(gam, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save_predictions(path, **predictions_dicts):
    check_dir_exists(path)
    for filename, predictions in predictions_dicts.items():
        with open(f"{path}/{filename}.pkl", "wb") as handle:
            pickle.dump(predictions, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save_stats(subdir, folder, **stats_dicts):
    for filename, data in stats_dicts.items():
        with open(f"{subdir}/{folder}/{filename}.pkl", "wb") as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


def save_with_cutoff_removed(
    basepath,
    predictions,
    predictions_r,
    darwin,
    predictions_f,
    predictions_rf,
    darwin_f,
    cutoff_summary,
    cutoff_summary_r,
    cutoff_summary_f,
    cutoff_summary_rf,
):
    subdir = check_dir_exists(f"{basepath}/t_cutoff")
    check_dir_exists(f"{subdir}/present")
    check_dir_exists(f"{subdir}/future")
    check_dir_exists(f"{subdir}/summaries")
    save_stats(
        f"{subdir}",
        "present",
        **{
            "predictions_cut": predictions,
            "predictions_cut_r": predictions_r,
            "darwin_cut": darwin,
        },
    )
    save_stats(
        f"{subdir}",
        "future",
        **{
            "predictions_cut_f": predictions_f,
            "predictions_cut_rf": predictions_rf,
            "darwin_cut_f": darwin_f,
        },
    )
    save_stats(
        f"{subdir}",
        "summaries",
        **{
            "cutoff_summary": cutoff_summary,
            "cutoff_summary_r": cutoff_summary_r,
            "cutoff_summary_f": cutoff_summary_f,
            "cutoff_summary_rf": cutoff_summary_rf,
        },
    )


def save_means_and_medians(
    basepath,
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
):
    subdir = check_dir_exists(f"{basepath}/t_stats")
    check_dir_exists(f"{subdir}/present")
    check_dir_exists(f"{subdir}/future")
    save_stats(
        f"{subdir}",
        "present",
        **{
            "mean_predictions": mean_predictions,
            "mean_predictions_r": mean_predictions_r,
            "mean_darwin": mean_darwin,
            "median_predictions": median_predictions,
            "median_predictions_r": median_predictions_r,
            "median_darwin": median_darwin,
        },
    )
    save_stats(
        f"{subdir}",
        "future",
        **{
            "mean_predictions_f": mean_predictions_f,
            "mean_predictions_rf": mean_predictions_rf,
            "mean_darwin_f": mean_darwin_f,
            "median_predictions_f": median_predictions_f,
            "median_predictions_rf": median_predictions_rf,
            "median_darwin_f": median_darwin_f,
        },
    )


def save_ratios(
    basepath,
    mean_ratios,
    median_ratios,
    mean_ratios_r,
    median_ratios_r,
    mean_ratios_f,
    median_ratios_f,
    mean_ratios_rf,
    median_ratios_rf,
):
    subdir = check_dir_exists(f"{basepath}/t_ratios")
    check_dir_exists(f"{subdir}/present")
    check_dir_exists(f"{subdir}/future")
    save_stats(
        f"{subdir}",
        "present",
        **{
            "mean_ratios": mean_ratios,
            "mean_ratios_r": mean_ratios_r,
            "median_ratios": median_ratios,
            "median_ratios_r": median_ratios_r,
        },
    )
    save_stats(
        f"{subdir}",
        "future",
        **{
            "mean_ratios_f": mean_ratios_f,
            "mean_ratios_rf": mean_ratios_rf,
            "median_ratios_f": median_ratios_f,
            "median_ratios_rf": median_ratios_rf,
        },
    )


def save_rsq(
    basepath,
    rsq,
    rsq_r,
    rsq_f,
    rsq_rf,
):
    subdir = check_dir_exists(f"{basepath}/t_rsquared")
    check_dir_exists(f"{subdir}/present")
    check_dir_exists(f"{subdir}/future")
    save_stats(
        f"{subdir}",
        "present",
        **{
            "rsq": rsq,
            "rsq_r": rsq_r,
        },
    )
    save_stats(
        f"{subdir}",
        "future",
        **{
            "rsq_f": rsq_f,
            "rsq_rf": rsq_rf,
        },
    )


def save_summaries(basepath, combined_df, summary, summary_r, summary_f, summary_rf):
    subdir = check_dir_exists(f"{basepath}/t_summary")
    combined_df.to_csv(f"{subdir}/summary_all.csv")
    save_stats(
        f"{basepath}",
        "t_summary",
        **{
            "summary": summary,
            "summary_r": summary_r,
            "summary_f": summary_f,
            "summary_rf": summary_rf,
        },
    )
