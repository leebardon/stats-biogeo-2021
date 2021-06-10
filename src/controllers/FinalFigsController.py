import time, os
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.models import Save
from src.models.gams import AnalyseGams
from src.views.ScatterPlots import ScatterSettings
from src.views.RelativeDiffMaps import DiffMapSettings
from src.views import (
    Maps,
    RelativeDiffMaps,
    ScatterPlots,
    Barplot,
)

base = Path(os.path.abspath(__file__)).parents[2]

PREDICTIONS = base / "results" / "gams_output" / "predictions"
DARWIN = base / "data" / "processed" / "validation_sets" / "plankton"
COORDS = base / "data" / "processed" / "model_ocean_data"
INNERPLOT_DATA = base / "results" / "analysis_output" / "summary"
PLOTS = base / "results" / "all_plots"
MAPS = Save.check_dir_exists(f"{PLOTS}/maps")
SCATTER = Save.check_dir_exists(f"{PLOTS}/scatter_plots")
DIFF = Save.check_dir_exists(f"{PLOTS}/relative_diff_maps")
INNER = Save.check_dir_exists(f"{PLOTS}/inner_plots")


config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(2)


print("Getting GAMs predictions and Darwin target data...")
with alive_bar(3) as bar:
    (
        predictions,
        predictions_r,
        predictions_f,
        predictions_rf,
    ) = AnalyseGams.get_predictions(
        f"{PREDICTIONS}",
        *[
            "predictions",
            "predictions_r",
            "predictions_f",
            "predictions_rf",
        ],
    )
    bar()
    t
    (darwin_ocean, darwin_ocean_f,) = AnalyseGams.get_targets(
        f"{DARWIN}",
        *[
            "plankton_oce",
            "plankton_oce_f",
        ],
    )
    bar()
    t
    coords = Maps.get_coords(COORDS)

    (summary, summary_r, summary_f, summary_rf) = Maps.get_inner(
        f"{INNERPLOT_DATA}",
        "summary.pkl",
        "summary_r.pkl",
        "summary_f.pkl",
        "summary_rf.pkl",
    )
    bar()
    t

print("Setting all values below cutoff equal to 1e-5 ...")
with alive_bar(1) as bar:
    all_plank_dicts = [
        predictions,
        predictions_r,
        predictions_f,
        predictions_rf,
        darwin_ocean,
        darwin_ocean_f,
    ]
    [Maps.below_cutoff_to_cutoff(plank_dict) for plank_dict in all_plank_dicts]
    bar()
    t

print("Calculate annual means and plotting maps - Darwin Model Ocean (1987-2008)...")
with alive_bar(1) as bar:

    MAPS_P = Save.check_dir_exists(f"{MAPS}/present")

    Maps.process_and_plot(
        darwin_ocean,
        coords,
        Save.check_dir_exists(f"{MAPS_P}/darwin"),
        "Darwin Model Ocean (1987-2008)",
    )
    bar()
    t

print(
    "Calculate annual means and plotting maps - GAMs Predictions from Ocean Measurements (1987-2008)..."
)
with alive_bar(1) as bar:
    Maps.process_and_plot(
        predictions,
        coords,
        Save.check_dir_exists(f"{MAPS_P}/gams_measurements"),
        "GAMs from Observations (1987-2008)",
    )
    bar()
    t

print(
    "Calculate annual means and plotting maps - GAMs Predictions from Random Samples (1987-2008)..."
)
with alive_bar(1) as bar:
    Maps.process_and_plot(
        predictions_r,
        coords,
        Save.check_dir_exists(f"{MAPS_P}/gams_random"),
        "GAMs from Random Sampling (1987-2008)",
    )
    bar()
    t


print("Calculate annual means and plotting maps - Darwin Model Ocean (2079-2100)...")
with alive_bar(1) as bar:

    MAPS_F = Save.check_dir_exists(f"{MAPS}/future")

    Maps.process_and_plot(
        darwin_ocean_f,
        coords,
        Save.check_dir_exists(f"{MAPS_F}/darwin"),
        "Darwin Model Ocean (2079-2100)",
    )
    bar()
    t

print(
    "Calculate annual means and plotting maps - GAMs Predictions from Ocean Measurements (2079-2100)..."
)
with alive_bar(1) as bar:
    Maps.process_and_plot(
        predictions_f,
        coords,
        Save.check_dir_exists(f"{MAPS_F}/gams_measurements"),
        "GAMs from Observations (2079-2100)",
    )
    bar()
    t

print(
    "Calculate annual means and plotting maps - GAMs Predictions from Random Sampling (2079-2100)..."
)
with alive_bar(1) as bar:
    Maps.process_and_plot(
        predictions_rf,
        coords,
        Save.check_dir_exists(f"{MAPS_F}/gams_random"),
        "GAMs from Random Sampling (2079-2100)",
    )
    bar()
    t

print("Plotting 1987-2008 Mean Relative Difference Maps (%)...")
with alive_bar(2) as bar:

    DMS = DiffMapSettings()
    DIFF_P = Save.check_dir_exists(f"{DIFF}/present")

    RelativeDiffMaps.generate_diff_maps(
        darwin_ocean,
        predictions,
        coords,
        Save.check_dir_exists(f"{DIFF_P}/gams"),
        "Mean Relative Difference",
        DMS.obvs,
    )
    bar()
    t
    RelativeDiffMaps.generate_diff_maps(
        darwin_ocean,
        predictions_r,
        coords,
        Save.check_dir_exists(f"{DIFF_P}/gams_random"),
        "Mean Relative Difference",
        DMS.rand,
    )
    bar()
    t

print("Plotting 2079-2100 Mean Relative Difference Maps (%)...")
with alive_bar(2) as bar:

    DIFF_F = Save.check_dir_exists(f"{DIFF}/future")

    RelativeDiffMaps.generate_diff_maps(
        darwin_ocean_f,
        predictions_f,
        coords,
        Save.check_dir_exists(f"{DIFF_F}/gams"),
        "Mean Relative Difference",
        DMS.obvs,
    )
    bar()
    t
    RelativeDiffMaps.generate_diff_maps(
        darwin_ocean_f,
        predictions_rf,
        coords,
        Save.check_dir_exists(f"{DIFF_F}/gams_random"),
        "Mean Relative Difference",
        DMS.rand,
    )
    bar()
    t

print("Plotting scatter plots (1987-2008)...")
with alive_bar(2) as bar:

    SETTINGS = ScatterSettings()
    SCATTER_P = Save.check_dir_exists(f"{SCATTER}/present")
    INNER_P = Save.check_dir_exists(f"{INNER}/present")

    ScatterPlots.generate_scatter_plots(
        predictions,
        darwin_ocean,
        summary,
        Save.check_dir_exists(f"{SCATTER_P}/measurements"),
        Save.check_dir_exists(f"{INNER_P}/measurements"),
        1,
        SETTINGS.present,
    )
    bar()
    t
    ScatterPlots.generate_scatter_plots(
        predictions_r,
        darwin_ocean,
        summary_r,
        Save.check_dir_exists(f"{SCATTER_P}/random"),
        Save.check_dir_exists(f"{INNER_P}/random"),
        1,
        SETTINGS.present,
    )
    bar()
    t

print("Plotting scatter plots (2079-2100)...")
with alive_bar(2) as bar:

    SCATTER_F = Save.check_dir_exists(f"{SCATTER}/future")
    INNER_F = Save.check_dir_exists(f"{INNER}/future")

    ScatterPlots.generate_scatter_plots(
        predictions_f,
        darwin_ocean_f,
        summary_f,
        Save.check_dir_exists(f"{SCATTER_F}/measurements"),
        Save.check_dir_exists(f"{INNER_F}/measurements"),
        2,
        SETTINGS.future,
    )
    bar()
    t
    ScatterPlots.generate_scatter_plots(
        predictions_rf,
        darwin_ocean_f,
        summary_rf,
        Save.check_dir_exists(f"{SCATTER_F}/random"),
        Save.check_dir_exists(f"{INNER_F}/random"),
        2,
        SETTINGS.future,
    )
    bar()
    t

print("Plotting comparative r^2, balanced acc. and means ratios bar chart...")
with alive_bar(2) as bar:

    Barplot.generate_barplot(
        Save.check_dir_exists(f"{PLOTS}/barplot"),
        summary,
        summary_f,
        summary_r,
        summary_rf,
    )
