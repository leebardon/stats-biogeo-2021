import pandas as pd
import statistics
import pickle


def get_predictions(path, *prediction_sets):
    p_sets = []
    for predictons in prediction_sets:
        with open(f"{path}/{predictons}.pkl", "rb") as handle:
            predictons_set = pickle.load(handle)
        p_sets.append(predictons_set)
    return [p_sets[i] for i in range(len(p_sets))]


def get_targets(path, *darwin_true_values):
    darwin_targets = []
    for target in darwin_true_values:
        with open(f"{path}/{target}.pkl", "rb") as handle:
            target_set = pickle.load(handle)
        darwin_targets.append(target_set)
    return [darwin_targets[i] for i in range(len(darwin_targets))]


def cut_off(predictions, target, cutoff):
    f_groups = ["Pro", "Pico", "Cocco", "Diazo", "Diatom", "Dino", "Zoo"]
    gams_presence, darwin_presence, total = [], [], len(target["Pro"])
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
    cutoffs["Means Ratios"] = means
    cutoffs["Medians Ratios"] = meds
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
