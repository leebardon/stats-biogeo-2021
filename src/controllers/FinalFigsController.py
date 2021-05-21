import time
import pickle
import os, sys
import numpy as np
import pandas as pd
from pathlib import Path
from alive_progress import alive_bar, config_handler

from src.views import (
    Maps,
    RelativeDiffMaps,
    ScatterPlots,
)

base_path = Path(os.path.abspath(__file__)).parents[1] / "all_outputs"

PREDICTIONS_PRESENT = base_path / "gams_output" / "predictions_present"
PREDICTIONS_FUTURE = base_path / "gams_output" / "predictions_future"
DARWIN_TARGET = base_path / "validation_sets" / "plankton"
COORDS_DEGREES = base_path / "model_whole_ocean_data" / "degrees_coords.pkl"
INNER_PLOT_DATA = base_path / "analysis_output" / "summary"

config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.05)


print("Getting GAMs predictions and Darwin target data...")
with alive_bar(5) as bar:
    with open(f"{PREDICTIONS_PRESENT}/predictions_p.pkl", "rb") as handle:
        gams_predictions_p = pickle.load(handle)
    with open(f"{PREDICTIONS_PRESENT}/predictions_random_p.pkl", "rb") as handle:
        gams_predictions_random_p = pickle.load(handle)
    bar()
    t
    with open(f"{PREDICTIONS_FUTURE}/predictions_f.pkl", "rb") as handle:
        gams_predictions_f = pickle.load(handle)
    with open(f"{PREDICTIONS_FUTURE}/predictions_random_f.pkl", "rb") as handle:
        gams_predictions_random_f = pickle.load(handle)
    bar()
    t
    with open(f"{DARWIN_TARGET}/plankton_ocean_present.pkl", "rb") as handle:
        darwin_target_p = pickle.load(handle)
    with open(f"{DARWIN_TARGET}/plankton_ocean_future.pkl", "rb") as handle:
        darwin_target_f = pickle.load(handle)
    bar()
    t
    with open(f"{COORDS_DEGREES}", "rb") as handle:
        coords = pickle.load(handle)
    bar()
    t
    with open(f"{INNER_PLOT_DATA}/summary_p.pkl", "rb") as handle:
        summary_p = pickle.load(handle)
    with open(f"{INNER_PLOT_DATA}/summary_rand_p.pkl", "rb") as handle:
        summary_rand_p = pickle.load(handle)
    bar()
    t
    with open(f"{INNER_PLOT_DATA}/summary_f.pkl", "rb") as handle:
        summary_f = pickle.load(handle)
    with open(f"{INNER_PLOT_DATA}/summary_rand_f.pkl", "rb") as handle:
        summary_rand_f = pickle.load(handle)
    bar()
    t


print("Setting all values below cutoff equal to zero...")
with alive_bar(1) as bar:
    all_plank_dicts = [
        gams_predictions_p,
        gams_predictions_random_p,
        gams_predictions_f,
        gams_predictions_random_f,
        darwin_target_p,
        darwin_target_f,
    ]
    [Maps.below_cutoff_to_zero(plank_dict) for plank_dict in all_plank_dicts]
    bar()
    t

# print("Calculate annual means and plotting maps - Darwin Model Ocean (1987-2008)...")
# with alive_bar(1) as bar:
#     Maps.process_and_plot(
#         darwin_target_p,
#         coords,
#         "/present/darwin",
#         "Darwin Model Ocean (1987-2008)",
#     )
#     bar()
#     t

# print(
#     "Calculate annual means and plotting maps - GAMs Predictions from Ocean Measurements (1987-2008)..."
# )
# with alive_bar(1) as bar:
#     Maps.process_and_plot(
#         gams_predictions_p,
#         coords,
#         "/present/gams_measurements",
#         "GAMs from Observations (1987-2008)",
#     )
#     bar()
#     t

# print(
#     "Calculate annual means and plotting maps - GAMs Predictions from Random Samples (1987-2008)..."
# )
# with alive_bar(1) as bar:
#     Maps.process_and_plot(
#         gams_predictions_random_p,
#         coords,
#         "/present/gams_random",
#         "GAMs from Random Sampling (1987-2008)",
#     )
#     bar()
#     t


# print("Calculate annual means and plotting maps - Darwin Model Ocean (2079-2100)...")
# with alive_bar(1) as bar:
#     Maps.process_and_plot(
#         darwin_target_f,
#         coords,
#         "/future/darwin",
#         "Darwin Model Ocean (2079-2100)",
#     )
#     bar()
#     t

# print(
#     "Calculate annual means and plotting maps - GAMs Predictions from Ocean Measurements (2079-2100)..."
# )
# with alive_bar(1) as bar:
#     Maps.process_and_plot(
#         gams_predictions_f,
#         coords,
#         "/future/gams_measurements",
#         "GAMs from Observations (2079-2100)",
#     )
#     bar()
#     t

# print(
#     "Calculate annual means and plotting maps - GAMs Predictions from Random Sampling (2079-2100)..."
# )
# with alive_bar(1) as bar:
#     Maps.process_and_plot(
#         gams_predictions_random_f,
#         coords,
#         "/future/gams_random",
#         "GAMs from Random Sampling (2079-2100)",
#     )
#     bar()
#     t

# print("Plotting 1987-2008 Mean Relative Difference Maps (%)...")
# with alive_bar(2) as bar:

#     RelativeDiffMaps.generate_diff_maps(
#         darwin_target_p,
#         gams_predictions_p,
#         coords,
#         "/present/gams",
#         "Mean Relative Difference",
#     )
#     bar()
#     t
#     RelativeDiffMaps.generate_diff_maps(
#         darwin_target_p,
#         gams_predictions_random_p,
#         coords,
#         "/present/gams_random",
#         "Mean Relative Difference",
#     )
#     bar()
#     t

# print("Plotting 2079-2100 Mean Relative Difference Maps (%)...")
# with alive_bar(2) as bar:
#     RelativeDiffMaps.generate_diff_maps(
#         darwin_target_f,
#         gams_predictions_f,
#         coords,
#         "/future/gams",
#         "Mean Relative Difference",
#     )
#     bar()
#     t
#     RelativeDiffMaps.generate_diff_maps(
#         darwin_target_f,
#         gams_predictions_random_f,
#         coords,
#         "/future/gams_random",
#         "Mean Relative Difference",
#     )
#     bar()
#     t

print("Plotting scatter plots (1987-2008)...")
with alive_bar(2) as bar:
    ScatterPlots.generate_plots(
        gams_predictions_p,
        darwin_target_p,
        summary_p,
        "/present/measurements",
    )
    bar()
    t
    ScatterPlots.generate_plots(
        gams_predictions_random_p,
        darwin_target_p,
        summary_rand_p,
        "/present/random",
    )
    bar()
    t

print("Plotting scatter plots (2079-2100)...")
with alive_bar(2) as bar:
    ScatterPlots.generate_plots(
        gams_predictions_f,
        darwin_target_f,
        summary_f,
        "/future/measurements",
    )
    bar()
    t
    ScatterPlots.generate_plots(
        gams_predictions_random_f,
        darwin_target_f,
        summary_rand_f,
        "/future/random",
    )
    bar()
    t
