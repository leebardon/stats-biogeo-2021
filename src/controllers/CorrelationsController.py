import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import time
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.models.correlations import Correlations
from src.models import Save
from src.views import HeatMaps


BASEPATH = Path(os.path.abspath(__file__)).parents[2]
DATASETS = f"{BASEPATH}/data/processed_test2"
CORRSAVE = Save.check_dir_exists(f"{DATASETS}/correlations")
PLOTSAVE = Save.check_dir_exists(f"{BASEPATH}/results_test2/all_plots/heatmaps")


config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.05)


print("Getting plankton and predictors sample sets...")
with alive_bar(2) as bar:
    planksets = f"{DATASETS}/sampled_plankton"
    (
        plankton,
        plankton_r,
        plankton_f,
        plankton_rf,
        r2_plankton,
        r3_plankton,
        r2_plankton_f,
        r3_plankton_f,
    ) = Correlations.get_sample_sets(
        f"{planksets}/plankton.pkl",
        f"{planksets}/plankton_r.pkl",
        f"{planksets}/plankton_f.pkl",
        f"{planksets}/plankton_rf.pkl",
        f"{planksets}/r2_plankton.pkl",
        f"{planksets}/r3_plankton.pkl",
        f"{planksets}/r2_plankton_f.pkl",
        f"{planksets}/r3_plankton_f.pkl",
    )
    bar()
    t
    predsets = f"{DATASETS}/sampled_predictors"
    (
        predictors,
        predictors_r,
        predictors_f,
        predictors_rf,
        r2_predictors,
        r3_predictors,
        r2_predictors_f,
        r3_predictors_f,
    ) = Correlations.get_sample_sets(
        f"{predsets}/predictors.pkl",
        f"{predsets}/predictors_r.pkl",
        f"{predsets}/predictors_f.pkl",
        f"{predsets}/predictors_rf.pkl",
        f"{predsets}/r2_predictors.pkl",
        f"{predsets}/r3_predictors.pkl",
        f"{predsets}/r2_predictors_f.pkl",
        f"{predsets}/r3_predictors_f.pkl",
    )
    bar()
    t

print("Calculating distance correlations...")
with alive_bar(4) as bar:
    dcorrs = Correlations.calculate_dcorrs(predictors, plankton)
    dcorrs_f = Correlations.calculate_dcorrs(predictors_f, plankton_f)
    bar()
    t
    dcorrs_r = Correlations.calculate_dcorrs(predictors_r, plankton_r)
    r2_dcorrs = Correlations.calculate_dcorrs(r2_predictors, r2_plankton)
    r3_dcorrs = Correlations.calculate_dcorrs(r3_predictors, r3_plankton)
    bar()
    t
    dcorrs_rf = Correlations.calculate_dcorrs(predictors_rf, plankton_rf)
    r2_dcorrs_f = Correlations.calculate_dcorrs(r2_predictors_f, r2_plankton_f)
    r3_dcorrs_f = Correlations.calculate_dcorrs(r3_predictors_f, r3_plankton_f)
    bar()
    t

    Save.save_to_pkl(
        Save.check_dir_exists(f"{CORRSAVE}/dcorrs"),
        **{
            "dcorrs.pkl": dcorrs,
            "dcorrs_r.pkl": dcorrs_r,
            "dcorrs_f.pkl": dcorrs_f,
            "dcorrs_rf.pkl": dcorrs_rf,
            "r2_dcorrs.pkl": r2_dcorrs,
            "r3_dcorrs.pkl": r3_dcorrs,
            "r2_dcorrs_f.pkl": r2_dcorrs_f,
            "r3_dcorrs_f.pkl": r3_dcorrs_f,
        },
    )
    bar()
    t


print("Calculating Pearson's correlation coefficients...")
with alive_bar(4) as bar:
    pearsons = Correlations.calculate_pearsons(predictors, plankton)
    pearsons_f = Correlations.calculate_pearsons(predictors_f, plankton_f)
    bar()
    t
    pearsons_r = Correlations.calculate_pearsons(predictors_r, plankton_r)
    r2_pearsons = Correlations.calculate_pearsons(r2_predictors, r2_plankton)
    r3_pearsons = Correlations.calculate_pearsons(r3_predictors, r3_plankton)
    bar()
    t
    pearsons_rf = Correlations.calculate_pearsons(predictors_rf, plankton_rf)
    r2_pearsons_f = Correlations.calculate_pearsons(r2_predictors_f, r2_plankton_f)
    r3_pearsons_f = Correlations.calculate_pearsons(r3_predictors_f, r3_plankton_f)
    bar()
    t

    Save.save_to_pkl(
        Save.check_dir_exists(f"{CORRSAVE}/pearsons"),
        **{
            "pearsons.pkl": pearsons,
            "pearsons_r.pkl": pearsons_r,
            "pearsons_f.pkl": pearsons_f,
            "pearsons_rf.pkl": pearsons_rf,
            "r2_pearsons.pkl": r2_pearsons,
            "r3_pearsons.pkl": r3_pearsons,
            "r2_pearsons_f.pkl": r2_pearsons_f,
            "r3_pearsons_f.pkl": r3_pearsons_f,
        },
    )
    bar()
    t

print("Calculating log transformed Pearson's correlation coefficients...")
with alive_bar(4) as bar:
    ln_pearsons = Correlations.calculate_ln_pearsons(predictors, plankton)
    ln_pearsons_f = Correlations.calculate_ln_pearsons(predictors_f, plankton_f)
    bar()
    t
    ln_pearsons_r = Correlations.calculate_ln_pearsons(predictors_r, plankton_r)
    ln_r2_pearsons = Correlations.calculate_ln_pearsons(r2_predictors, r2_plankton)
    ln_r3_pearsons = Correlations.calculate_ln_pearsons(r3_predictors, r3_plankton)
    bar()
    t
    ln_pearsons_rf = Correlations.calculate_ln_pearsons(predictors_rf, plankton_rf)
    ln_r2_pearsons_f = Correlations.calculate_ln_pearsons(
        r2_predictors_f, r2_plankton_f
    )
    ln_r3_pearsons_f = Correlations.calculate_ln_pearsons(
        r3_predictors_f, r3_plankton_f
    )
    bar()
    t

    Save.save_to_pkl(
        Save.check_dir_exists(f"{CORRSAVE}/ln_pearsons"),
        **{
            "ln_pearsons.pkl": ln_pearsons,
            "ln_pearsons_r.pkl": ln_pearsons_r,
            "ln_pearsons_f.pkl": ln_pearsons_f,
            "ln_pearsons_rf.pkl": ln_pearsons_rf,
            "ln_r2_pearsons.pkl": ln_r2_pearsons,
            "ln_r3_pearsons.pkl": ln_r3_pearsons,
            "ln_r2_pearsons_f.pkl": ln_r2_pearsons_f,
            "ln_r3_pearsons_f.pkl": ln_r3_pearsons_f,
        },
    )
    bar()
    t

print("Calculating Spearman's Rank correlations...")
with alive_bar(4) as bar:
    spearmans = Correlations.calculate_spearmans(predictors, plankton)
    spearmans_f = Correlations.calculate_spearmans(predictors_f, plankton_f)
    bar()
    t
    spearmans_r = Correlations.calculate_spearmans(predictors_r, plankton_r)
    r2_spearmans = Correlations.calculate_spearmans(r2_predictors, r2_plankton)
    r3_spearmans = Correlations.calculate_spearmans(r3_predictors, r3_plankton)
    bar()
    t
    spearmans_rf = Correlations.calculate_spearmans(predictors_rf, plankton_rf)
    r2_spearmans_f = Correlations.calculate_spearmans(r2_predictors_f, r2_plankton_f)
    r3_spearmans_f = Correlations.calculate_spearmans(r3_predictors_f, r3_plankton_f)
    bar()
    t

    Save.save_to_pkl(
        Save.check_dir_exists(f"{CORRSAVE}/spearmans"),
        **{
            "spearmans.pkl": spearmans,
            "spearmans_r.pkl": spearmans_r,
            "spearmans_f.pkl": spearmans_f,
            "spearmans_rf.pkl": spearmans_rf,
            "r2_spearmans.pkl": r2_spearmans,
            "r3_spearmans.pkl": r3_spearmans,
            "r2_spearmans_f.pkl": r2_spearmans_f,
            "r3_spearmans_f.pkl": r3_spearmans_f,
        },
    )
    bar()
    t
breakpoint()
print("Plotting Distance Correlation heatmaps...")
with alive_bar(1) as bar:

    HeatMaps.correlation_heatmap(
        "coolwarm",
        Save.check_dir_exists(f"{PLOTSAVE}/dcorrs"),
        **{
            "hmap_dcorrs": dcorrs,
            "hmap_dcorrs_r": dcorrs_r,
            "hmap_dcorrs_f": dcorrs_f,
            "hmap_dcorrs_rf": dcorrs_rf,
        },
    )
    bar()
    t

print("Plotting Pearson's Correlation heatmaps...")
with alive_bar(1) as bar:

    HeatMaps.correlation_heatmap(
        "RdYlGn",
        Save.check_dir_exists(f"{PLOTSAVE}/pearsons"),
        **{
            "hmap_pearsons": pearsons,
            "hmap_pearsons_r": pearsons_r,
            "hmap_pearsons_f": pearsons_f,
            "hmap_pearsons_rf": pearsons_rf,
        },
    )
    bar()
    t

print("Plotting log transformed Pearson's Correlation heatmaps...")
with alive_bar(1) as bar:

    HeatMaps.correlation_heatmap(
        "Blues",
        Save.check_dir_exists(f"{PLOTSAVE}/ln_pearsons"),
        **{
            "hmap_ln_pearsons": ln_pearsons,
            "hmap_ln_pearsons_r": ln_pearsons_r,
            "hmap_ln_pearsons_f": ln_pearsons_f,
            "hmap_ln_pearsons_rf": ln_pearsons_rf,
        },
    )
    bar()
    t

print("Plotting Spearman's Correlation heatmaps...")
with alive_bar(1) as bar:

    HeatMaps.correlation_heatmap(
        "pink",
        Save.check_dir_exists(f"{PLOTSAVE}/spearmans"),
        **{
            "hmap_spearmans": spearmans,
            "hmap_spearmans_r": spearmans_r,
            "hmap_spearmans_f": spearmans_f,
            "hmap_spearmans_rf": spearmans_rf,
        },
    )
    bar()
    t
