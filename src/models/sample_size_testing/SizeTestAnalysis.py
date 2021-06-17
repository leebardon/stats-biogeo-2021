
import numpy as np
import pandas as pd
import itertools
from src.models.gams import AnalyseGams

CUTOFF = 1.001e-5

def pres_abs_summary(gams, darwin, CELLS, ptype, fut=""):
    total = len(darwin["Pro"])
    try:
        gams[f"coccos{fut}_0"]
        GROUPS = [f"coccos{fut}_{i}" for i in np.arange(18)]
        darwin = list(itertools.repeat(darwin["Cocco"], 18))
    except:
        GROUPS = [f"diatoms{fut}_{i}" for i in np.arange(18)]
        darwin = list(itertools.repeat(darwin["Diatom"], 18))

    true_pos = [AnalyseGams.true_positive(gams[g], darwin[i]) for i, g in enumerate(GROUPS)]
    true_neg = [AnalyseGams.true_negative(gams[g], darwin[i]) for i, g in enumerate(GROUPS)]
    false_pos = [AnalyseGams.false_positive(gams[g], darwin[i]) for i, g in enumerate(GROUPS)]
    false_neg = [AnalyseGams.false_negative(gams[g], darwin[i]) for i, g in enumerate(GROUPS)]
    gams_pres = [(gams[g][(gams[g] > CUTOFF) & (darwin[i] > CUTOFF)]) for i, g in enumerate(GROUPS)]
    darwin_pres = [
        (darwin[i][(darwin[i] > CUTOFF) & (gams[g] > CUTOFF)]) for i, g in enumerate(GROUPS)
    ]
    gams_abs = [(gams[g][(gams[g] < CUTOFF)]) for g in GROUPS]
    darwin_abs = [(darwin[i][(darwin[i] < CUTOFF)]) for i, g in enumerate(GROUPS)]
    summary = pres_abs_summary_df(
        gams_abs,
        darwin_abs,
        gams_pres,
        darwin_pres,
        true_pos,
        true_neg,
        false_pos,
        false_neg,
        total,
        CELLS,
        ptype,
    )
    # gams_prepped, darwin_prepped = remove_outliers(gams_pres, darwin_pres)
    return gams_pres, darwin_pres, summary


def remove_outliers(gams, darwin):
    for i in range(len(gams)):
        g_max, d_max = AnalyseGams.get_max(gams[i], darwin[i])
        darwin[i] = np.where(darwin[i] > d_max, d_max, darwin[i])
        gams[i] = np.where(gams[i] > g_max, g_max, gams[i])
    return gams, darwin


def calc_ratios(mean_gams, med_gams, mean_dar, med_dar):
    mean_ratios, med_ratios = [], []
    for i in range(len(med_gams)):
        mean_ratios.append(round((mean_gams[i] - mean_dar) / mean_dar, 2))
        med_ratios.append(round((med_gams[i] - med_dar) / med_dar, 2))
    return mean_ratios, med_ratios



def pres_abs_summary_df(
    gams_abs,
    darwin_abs,
    gams_pres,
    darwin_pres,
    true_pos,
    true_neg,
    false_pos,
    false_neg,
    total,
    CELLS,
    ptype,
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
    index = [f"{ptype}_{i}" for i in CELLS]
    summary = pd.DataFrame(columns=cols, index=index)
    for i in range(len(index)):
        summary["Darwin < cutoff"][i] = len(darwin_abs[i])
        summary["GAMs < cutoff"][i] = len(gams_abs[i])
        summary["Both > cutoff"][i] = len(gams_pres[i])
        summary["True Pos."][i] = len(true_pos[i])
        summary["True Neg."][i] = len(true_neg[i])
        summary["False Pos."][i] = len(false_pos[i])
        summary["False Neg."][i] = len(false_neg[i])
        summary["Sensitivity"][i] = AnalyseGams.sensitivity(true_pos[i], gams_abs[i], total)
        summary["Specificity"][i] = AnalyseGams.specificity(true_neg[i], gams_abs[i])
        summary["Balanced Acc."][i] = (
            summary["Sensitivity"][i] + summary["Specificity"][i]
        ) / 2
        summary["Presence Frac."][i] = 1 - (total - len(true_pos[i])) / total

    return summary


def return_summary(cutoffs_df, means_ratios, meds_ratios, rsq):
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
            "Rand. (1987-2008)",
            "Rand. (1987-2008)",
            "Rand. (2079-2100)",
            "Rand. (2079-2100)",
        ],
        axis=0,
    )