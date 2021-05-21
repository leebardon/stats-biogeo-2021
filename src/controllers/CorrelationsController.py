import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import time
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.models.correlations import Correlations
from src.models import Save
from src.views import HeatMaps


BASEPATH = Path(os.path.abspath(__file__)).parents[2]
DATASETS = f"{BASEPATH}/data/processed"
CORRSAVE = Save.check_dir_exists(f"{DATASETS}/correlations")
PLOTSAVE = Save.check_dir_exists(f"{BASEPATH}/results/all_plots/heatmaps")


config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.05)


print("Getting plankton and predictors sample sets...")
with alive_bar(2) as bar:
    plankton, plankton_r, plankton_f, plankton_r_f = Correlations.get_sample_sets(
        f"{DATASETS}/sampled_plankton/plankton.pkl",
        f"{DATASETS}/sampled_plankton/plankton_r.pkl",
        f"{DATASETS}/sampled_plankton/plankton_f.pkl",
        f"{DATASETS}/sampled_plankton/plankton_r_f.pkl",
    )
    bar()
    t
    (
        predictors,
        predictors_r,
        predictors_f,
        predictors_r_f,
    ) = Correlations.get_sample_sets(
        f"{DATASETS}/sampled_predictors/predictors_X.pkl",
        f"{DATASETS}/sampled_predictors/rand_predictors_X.pkl",
        f"{DATASETS}/sampled_predictors/predictors_X_f.pkl",
        f"{DATASETS}/sampled_predictors/rand_predictors_X_f.pkl",
    )
    bar()
    t

print("Calculating distance correlations...")
with alive_bar(4) as bar:
    dcorrs = Correlations.calculate_dcorrs(predictors, plankton)
    bar()
    t
    dcorrs_r = Correlations.calculate_dcorrs(predictors_r, plankton_r)
    bar()
    t
    dcorrs_f = Correlations.calculate_dcorrs(predictors_f, plankton_f)
    bar()
    t
    dcorrs_r_f = Correlations.calculate_dcorrs(predictors_r_f, plankton_r_f)

    Save.save_to_pkl(
        f"{CORRSAVE}/dcorrs",
        **{
            "dcorrs.pkl": dcorrs,
            "dcorrs_r.pkl": dcorrs_r,
            "dcorrs_f.pkl": dcorrs_f,
            "dcorrs_r_f.pkl": dcorrs_r_f,
        },
    )
    bar()
    t


print("Calculating Pearson's correlation coefficients...")
with alive_bar(4) as bar:
    pearsons = Correlations.calculate_pearsons(predictors, plankton)
    bar()
    t
    pearsons_r = Correlations.calculate_pearsons(predictors_r, plankton_r)
    bar()
    t
    pearsons_f = Correlations.calculate_pearsons(predictors_f, plankton_f)
    bar()
    t
    pearsons_r_f = Correlations.calculate_pearsons(predictors_r_f, plankton_r_f)

    Save.save_to_pkl(
        f"{CORRSAVE}/pearsons",
        **{
            "pearsons.pkl": pearsons,
            "pearsons_r.pkl": pearsons_r,
            "pearsons_f.pkl": pearsons_f,
            "pearsons_r_f.pkl": pearsons_r_f,
        },
    )
    bar()
    t

print("Calculating log transformed Pearson's correlation coefficients...")
with alive_bar(4) as bar:
    ln_pearsons = Correlations.calculate_ln_pearsons(predictors, plankton)
    bar()
    t
    ln_pearsons_r = Correlations.calculate_ln_pearsons(predictors_r, plankton_r)
    bar()
    t
    ln_pearsons_f = Correlations.calculate_ln_pearsons(predictors_f, plankton_f)
    bar()
    t
    ln_pearsons_r_f = Correlations.calculate_ln_pearsons(predictors_r_f, plankton_r_f)

    Save.save_to_pkl(
        f"{CORRSAVE}/ln_pearsons",
        **{
            "ln_pearsons.pkl": ln_pearsons,
            "ln_pearsons_r.pkl": ln_pearsons_r,
            "ln_pearsons_f.pkl": ln_pearsons_f,
            "ln_pearsons_r_f.pkl": ln_pearsons_r_f,
        },
    )
    bar()
    t

print("Calculating Spearman's Rank correlations...")
with alive_bar(4) as bar:
    spearmans = Correlations.calculate_spearmans(predictors, plankton)
    bar()
    t
    spearmans_r = Correlations.calculate_spearmans(predictors_r, plankton_r)
    bar()
    t
    spearmans_f = Correlations.calculate_spearmans(predictors_f, plankton_f)
    bar()
    t
    spearmans_r_f = Correlations.calculate_spearmans(predictors_r_f, plankton_r_f)

    Save.save_to_pkl(
        f"{CORRSAVE}/spearmans",
        **{
            "spearmans.pkl": spearmans,
            "spearmans_r.pkl": spearmans_r,
            "spearmans_f.pkl": spearmans_f,
            "spearmans_r_f.pkl": spearmans_r_f,
        },
    )
    bar()
    t

print("Plotting Distance Correlation heatmaps...")
with alive_bar(1) as bar:

    HeatMaps.correlation_heatmap(
        "coolwarm",
        f"{PLOTSAVE}/dcorrs",
        **{
            "hmap_dcorrs": dcorrs,
            "hmap_dcorrs_r": dcorrs_r,
            "hmap_dcorrs_f": dcorrs_f,
            "hmap_dcorrs_r_f": dcorrs_r_f,
        },
    )
    bar()
    t

print("Plotting Pearson's Correlation heatmaps...")
with alive_bar(1) as bar:

    HeatMaps.correlation_heatmap(
        "RdYlGn",
        f"{PLOTSAVE}/pearsons",
        **{
            "hmap_pearsons": pearsons,
            "hmap_pearsons_r": pearsons_r,
            "hmap_pearsons_f": pearsons_f,
            "hmap_pearsons_r_f": pearsons_r_f,
        },
    )
    bar()
    t

print("Plotting log transformed Pearson's Correlation heatmaps...")
with alive_bar(1) as bar:

    HeatMaps.correlation_heatmap(
        "Blues",
        f"{PLOTSAVE}/ln_pearsons",
        **{
            "hmap_ln_pearsons": ln_pearsons,
            "hmap_ln_pearsons_r": ln_pearsons_r,
            "hmap_ln_pearsons_f": ln_pearsons_f,
            "hmap_ln_pearsons_r_f": ln_pearsons_r_f,
        },
    )
    bar()
    t

print("Plotting Spearman's Correlation heatmaps...")
with alive_bar(1) as bar:

    HeatMaps.correlation_heatmap(
        "pink",
        f"{PLOTSAVE}/spearmans",
        **{
            "hmap_spearmans": spearmans,
            "hmap_spearmans_r": spearmans_r,
            "hmap_spearmans_f": spearmans_f,
            "hmap_spearmans_r_f": spearmans_r_f,
        },
    )
    bar()
    t
