import pandas as pd
import numpy as np
import pickle

F_GROUPS = ["Pro", "Pico", "Cocco", "Diazo", "Diatom", "Dino", "Zoo"]
CUTOFF = 1.001e-5


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


def pres_abs_summary(gams, darwin):
    total = len(darwin["Pro"])
    true_pos = [true_positive(gams[g], darwin[g]) for g in F_GROUPS]
    true_neg = [true_negative(gams[g], darwin[g]) for g in F_GROUPS]
    false_pos = [false_positive(gams[g], darwin[g]) for g in F_GROUPS]
    false_neg = [false_negative(gams[g], darwin[g]) for g in F_GROUPS]
    gams_pres = [(gams[g][(gams[g] > CUTOFF) & (darwin[g] > CUTOFF)]) for g in F_GROUPS]
    darwin_pres = [
        (darwin[g][(darwin[g] > CUTOFF) & (gams[g] > CUTOFF)]) for g in F_GROUPS
    ]
    gams_abs = [(gams[g][(gams[g] < CUTOFF)]) for g in F_GROUPS]
    darwin_abs = [(darwin[g][(darwin[g] < CUTOFF)]) for g in F_GROUPS]
    summary = summary_df(
        gams_abs,
        darwin_abs,
        gams_pres,
        darwin_pres,
        true_pos,
        true_neg,
        false_pos,
        false_neg,
        total,
    )
    # gams_prepped, darwin_prepped = remove_outliers(gams_pres, darwin_pres)
    return gams_pres, darwin_pres, summary


def remove_outliers(gams, darwin):
    for i in range(len(darwin)):
        g_max, d_max = get_max(gams[i], darwin[i])
        darwin[i] = np.where(darwin[i] > d_max, d_max, darwin[i])
        gams[i] = np.where(gams[i] > g_max, g_max, gams[i])
    return gams, darwin


def get_max(gams, darwin):
    return np.percentile(gams, 99.9), np.percentile(darwin, 99.9)


def true_positive(gams, darwin):
    return gams[(gams > CUTOFF) & (darwin > CUTOFF)]


def true_negative(gams, darwin):
    return gams[(gams <= CUTOFF) & (darwin <= CUTOFF)]


def false_positive(gams, darwin):
    return gams[(gams > CUTOFF) & (darwin <= CUTOFF)]


def false_negative(gams, darwin):
    return gams[(gams <= CUTOFF) & (darwin > CUTOFF)]


def summary_df(
    gams_abs,
    darwin_abs,
    gams_pres,
    darwin_pres,
    true_pos,
    true_neg,
    false_pos,
    false_neg,
    total,
):
    cols = [
        "Darwin < cutoff",
        "GAMs < cutoff",
        "Both > cutoff",
        "True Pos.",
        "True Neg.",
        "False Pos.",
        "False Neg.",
        "Sensitivity",
        "Specificity",
        "Balanced Acc.",
        "Presence Frac.",
    ]
    summary = pd.DataFrame(columns=cols, index=F_GROUPS)
    for i in range(len(F_GROUPS)):
        summary["Darwin < cutoff"][i] = len(darwin_abs[i])
        summary["GAMs < cutoff"][i] = len(gams_abs[i])
        summary["Both > cutoff"][i] = len(gams_pres[i])
        summary["True Pos."][i] = len(true_pos[i])
        summary["True Neg."][i] = len(true_neg[i])
        summary["False Pos."][i] = len(false_pos[i])
        summary["False Neg."][i] = len(false_neg[i])
        summary["Sensitivity"][i] = sensitivity(true_pos[i], gams_abs[i], total)
        summary["Specificity"][i] = specificity(true_neg[i], gams_abs[i])
        summary["Balanced Acc."][i] = (
            summary["Sensitivity"][i] + summary["Specificity"][i]
        ) / 2
        summary["Presence Frac."][i] = 1 - (total - len(true_pos[i])) / total

    return summary


def sensitivity(true_pos, gams_below, total):
    return len(true_pos) / (total - len(gams_below))


def specificity(true_neg, gams_below):
    return len(true_neg) / (len(gams_below))


def mean_and_median(predictions):
    means, medians = [], []
    for f_group in predictions:
        means.append(np.mean(f_group))
        medians.append(np.median(f_group))
    return means, medians


def calc_ratios(mean_gams, med_gams, mean_dar, med_dar):
    mean_ratios, med_ratios = [], []
    for i in range(len(med_gams)):
        mean_ratios.append(round((mean_gams[i] - mean_dar[i]) / mean_dar[i], 2))
        med_ratios.append(round((med_gams[i] - med_dar[i]) / med_dar[i], 2))
    return mean_ratios, med_ratios


def r_squared(darwin, gams):
    return [calc_rsq(darwin[i], gams[i]) for i in range(len(darwin))]


def calc_rsq(darwin, gams):
    residuals = calc_residuals(darwin, gams)
    data_var = calc_variance(darwin)
    residuals_var = calc_variance(residuals)
    return 1 - residuals_var / data_var


def calc_residuals(darwin, gams):
    return darwin - gams


def calc_variance(data):
    sq_diff = (data - data.mean()) ** 2
    return sq_diff.mean()


def return_summary(cutoffs_df, means_ratios, meds_ratios, rsq, total):
    cols = [
        "GAMs < cutoff",
        "Darwin < cutoff",
        "Both > cutoff",
        "Sensitivity",
        "Specificity",
        "Balanced Acc.",
    ]
    final_summary = cutoffs_df[cols].round(2)
    final_summary["Means Ratios"] = means_ratios
    final_summary["Medians Ratios"] = meds_ratios
    final_summary["r-squared"] = [round(r, 2) for r in rsq]
    return final_summary


def return_combined_df(dfs):
    return pd.concat(
        [df.rename(columns=lambda x: x.zfill(4)) for df in dfs],
        keys=[
            "Obvs. (1987-2008)",
            "Rand. (1987-2008)",
            "Obvs. (2079-2100)",
            "Rand. (2079-2100)",
        ],
        axis=0,
    )


def pres_abs_tsets(gams):
    absence = []
    for i in gams:
        absence.append(len(gams[i][gams[i] < 1.001e-5]))
    return absence
