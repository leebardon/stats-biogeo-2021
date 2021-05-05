import pandas as pd
import statistics
import pickle
from prettytable import PrettyTable


def cut_off(predictions, target, cutoff):
    f_groups = ["proko", "pico", "cocco", "diazo", "diatom", "dino", "zoo"]
    gams_presence, darwin_presence, total = [], [], len(target["proko"])
    gams_absence, darwin_absence, either_below_cutoff = [], [], []
    for group in f_groups:
        gams_presence.append(
            predictions[group][
                (predictions[group] >= cutoff) & (target[group] >= cutoff)
            ]
        )
        darwin_presence.append(
            target[group][(target[group] >= cutoff) & (predictions[group] >= cutoff)]
        )
        gams_absence.append(predictions[group][(predictions[group] < cutoff)])
        darwin_absence.append(target[group][(target[group] < cutoff)])

    [
        either_below_cutoff.append(total - len(gams_presence[i]))
        for i in range(len(f_groups))
    ]

    cutoff_summary_df = cutoff_summary(
        gams_absence, darwin_absence, either_below_cutoff, f_groups, total
    )

    return gams_presence, darwin_presence, cutoff_summary_df


def cutoff_summary(gams, darwin, either, f_groups, total):
    cutoff_summary = pd.DataFrame(
        {"Darwin < cutoff": [0], "GAMs < cutoff": [0], "Either < cutoff": [0]},
        index=f_groups,
    )
    for i in range(len(f_groups)):
        cutoff_summary["Darwin < cutoff"][i] = len(darwin[i])
        cutoff_summary["GAMs < cutoff"][i] = len(gams[i])
        cutoff_summary["Either < cutoff"][i] = either[i]

    cutoff_summary["Presence Fraction"] = 1 - (
        round(cutoff_summary["Either < cutoff"] / (2223085), 2)
    )

    return cutoff_summary


def mean_and_median(plankton_data, mean_arr, med_arr):
    for plankton in plankton_data:
        mean_arr.append(statistics.mean(plankton))
        med_arr.append(statistics.median(plankton))

    return mean_arr, med_arr


def calc_ratios(mean_gams, mean_darwin, med_gams, med_darwin, mean_ratios, med_ratios):
    for i in range(len(med_gams)):
        mean_r = round((mean_gams[i] - mean_darwin[i]) / mean_darwin[i], 2)
        med_r = round((med_gams[i] - med_darwin[i]) / med_darwin[i], 2)
        mean_ratios.append(mean_r)
        med_ratios.append(med_r)

    return mean_ratios, med_ratios


def save_as_dict(base_save_path, data, folder, filename):
    save_dict = {
        "proko": data[0],
        "pico": data[1],
        "cocco": data[2],
        "diazo": data[3],
        "diatom": data[4],
        "dino": data[5],
        "zoo": data[6],
    }

    with open(f"{base_save_path}/{folder}/{filename}.pkl", "wb") as handle:
        pickle.dump(save_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def r_squared(darwin_target, gams_predictions):
    rsq = []
    for i in range(len(darwin_target)):
        rsq.append(calc_rsq(darwin_target[i], gams_predictions[i]))

    return rsq


def calc_rsq(target, predictions):
    residuals = calc_residuals(target, predictions)
    data_var = calc_variance(target)
    residuals_var = calc_variance(residuals)
    rsq = 1 - (residuals_var) / (data_var)
    return rsq


def calc_residuals(target, predictions):
    residuals = target - predictions
    return residuals


def calc_variance(data):
    sq_diff = (data - data.mean()) ** 2
    variance = sq_diff.mean()
    return variance


def summary_df(cutoffs, means, meds, rsq, total):
    cols = ["Darwin < cutoff", "GAMs < cutoff", "Either < cutoff"]
    for col in cols:
        cutoffs[col] = fractions(cutoffs[col], total)
    cutoffs["Means Ratios"] = means.values()
    cutoffs["Medians Ratios"] = meds.values()
    cutoffs["r-squared"] = [round(r, 2) for r in rsq]
    summary_df = cutoffs

    return summary_df


def fractions(series, total):
    series = round((series / total), 2)
    return series


def combined_df(dfs):
    df_combined = pd.concat(
        [df.rename(columns=lambda x: x.zfill(4)) for df in dfs],
        keys=[
            "Obvs. (1987-2008)",
            "Rand. (1987-2008)",
            "Obvs. (2079-2100)",
            "Rand. (2079-2100)",
        ],
        axis=0,
    )

    return df_combined


def save_with_cutoff_removed(
    path,
    gams_p,
    gams_r_p,
    dar_p,
    dar_r_p,
    gams_f,
    gams_r_f,
    dar_f,
    dar_r_f,
    path_pres,
    path_fut,
):
    save_as_dict(path, gams_p, path_pres, "gams_cut_p")
    save_as_dict(path, gams_r_p, path_pres, "gams_rand_cut_p")
    save_as_dict(path, dar_p, path_pres, "darwin_cut_p")
    save_as_dict(path, dar_r_p, path_pres, "darwin_cut_rand_p")
    save_as_dict(path, gams_f, path_fut, "gams_cut_f")
    save_as_dict(path, gams_r_f, path_fut, "gams_rand_cut_f")
    save_as_dict(path, dar_f, path_fut, "darwin_cut_f")
    save_as_dict(path, dar_r_f, path_fut, "darwin_cut_rand_f")


def save_means_and_medians(
    path,
    mean_g_p,
    med_g_p,
    mean_g_r_p,
    med_g_r_p,
    mean_d_p,
    med_d_p,
    mean_g_f,
    med_g_f,
    mean_g_r_f,
    med_g_r_f,
    mean_d_f,
    med_d_f,
    path_mean_p,
    path_med_p,
    path_mean_f,
    path_med_f,
):
    save_as_dict(path, mean_g_p, path_mean_p, "means_gams_p")
    save_as_dict(path, med_g_p, path_med_p, "meds_gams_p")
    save_as_dict(path, mean_g_r_p, path_mean_p, "means_gams_rand_p")
    save_as_dict(path, med_g_r_p, path_med_p, "meds_gams_rand_p")
    save_as_dict(path, mean_d_p, path_mean_p, "means_darwin_p")
    save_as_dict(path, med_d_p, path_med_p, "meds_darwin_p")
    save_as_dict(path, mean_g_f, path_mean_f, "means_gams_f")
    save_as_dict(path, mean_g_r_f, path_med_f, "meds_gams_f")
    save_as_dict(path, mean_g_f, path_mean_f, "means_gams_rand_f")
    save_as_dict(path, mean_g_r_f, path_med_f, "meds_gams_rand_f")
    save_as_dict(path, mean_d_f, path_mean_f, "means_darwin_f")
    save_as_dict(path, med_d_f, path_med_f, "meds_darwin_f")


def save_ratios(
    path,
    mean_r_p,
    med_r_p,
    mean_r_rand_p,
    med_r_rand_p,
    mean_r_f,
    med_r_f,
    mean_r_rand_f,
    med_r_rand_f,
    path_ratio_p,
    path_ratio_f,
):
    save_as_dict(path, mean_r_p, path_ratio_p, "means_ratios_p")
    save_as_dict(path, med_r_p, path_ratio_p, "meds_ratios_p")
    save_as_dict(path, mean_r_rand_p, path_ratio_p, "means_ratios_rand_p")
    save_as_dict(path, med_r_rand_p, path_ratio_p, "meds_ratios_rand_p")
    save_as_dict(path, mean_r_f, path_ratio_f, "means_ratios_f")
    save_as_dict(path, med_r_f, path_ratio_f, "meds_ratios_f")
    save_as_dict(path, mean_r_rand_f, path_ratio_f, "means_ratios_rand_f")
    save_as_dict(path, med_r_rand_f, path_ratio_f, "meds_ratios_rand_f")
