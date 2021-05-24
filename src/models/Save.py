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


def save_with_cutoff_removed(
    basepath,
    predictions,
    predictions_r,
    darwin,
    predictions_f,
    predictions_rf,
    darwin_f,
):
    subdir = check_dir_exists(f"{basepath}/t_cutoff")
    pres_path = check_dir_exists(f"{subdir}/present")
    fut_path = check_dir_exists(f"{subdir}/future")
    plankton_dicts(
        f"{basepath}",
        **{
            f"{pres_path}/predictions_cut": predictions,
            f"{pres_path}/predictions_cut_r": predictions_r,
            f"{pres_path}/darwin_cut": darwin,
            f"{fut_path}/predictions_cut_f": predictions_f,
            f"{fut_path}/predictions_cut_rf": predictions_rf,
            f"{fut_path}/darwin_cut_f": darwin_f,
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
    pres_path = check_dir_exists(f"{subdir}/present")
    fut_path = check_dir_exists(f"{subdir}/future")
    plankton_dicts(
        f"{basepath}",
        **{
            f"{pres_path}/means/mean_predictions": mean_predictions,
            f"{pres_path}/means/mean_predictions_r": mean_predictions_r,
            f"{pres_path}/means/mean_darwin": mean_darwin,
            f"{fut_path}/means/mean_predictions_f": mean_predictions_f,
            f"{fut_path}/means/mean_predictions_rf": mean_predictions_rf,
            f"{fut_path}/means/mean_darwin_f": mean_darwin_f,
            f"{pres_path}/medians/median_predictions": median_predictions,
            f"{pres_path}/medians/median_predictions_r": median_predictions_r,
            f"{pres_path}/medians/median_darwin": median_darwin,
            f"{fut_path}/medians/median_predictions_f": median_predictions_f,
            f"{fut_path}/medians/median_predictions_rf": median_predictions_rf,
            f"{fut_path}/medians/median_dawrin_f": median_darwin_f,
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
    pres_path = check_dir_exists(f"{subdir}/present")
    fut_path = check_dir_exists(f"{subdir}/future")
    plankton_dicts(
        f"{basepath}",
        **{
            f"{pres_path}/mean_ratios": mean_ratios,
            f"{pres_path}/mean_ratios_r": mean_ratios_r,
            f"{fut_path}/mean_ratios_f": mean_ratios_f,
            f"{fut_path}/mean_ratios_rf": mean_ratios_rf,
            f"{pres_path}/median_ratios": median_ratios,
            f"{pres_path}/median_ratios_r": median_ratios_r,
            f"{fut_path}/median_ratios_f": median_ratios_f,
            f"{fut_path}/median_ratios_rf": median_ratios_rf,
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
    pres_path = check_dir_exists(f"{subdir}/present")
    fut_path = check_dir_exists(f"{subdir}/future")
    plankton_dicts(
        f"{basepath}",
        **{
            f"{pres_path}/rsq": rsq,
            f"{pres_path}/rsq_r": rsq_r,
            f"{fut_path}/rsq_f": rsq_f,
            f"{fut_path}/rsq_rf": rsq_rf,
        },
    )
