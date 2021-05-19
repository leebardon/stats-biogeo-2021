import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import xarray as xr
import time
from pathlib import Path
from random import randint
from alive_progress import alive_bar, config_handler
from src.views import MatrixPlots
from src.models import Save
from src.models.sample_measurements import (
    CleanData,
    AddMonthsColumn,
    CreateSamplingMatrix,
)

base_path = Path(os.path.abspath(__file__)).parents[2]
OCEAN_OBVS = base_path / "data" / "raw" / "ocean_observations.netcdf"
GRID_CELL = base_path / "data" / "raw" / "grid_igsm.nc"
SAVEPATH = base_path / "data" / "processed"
PLOTPATH = base_path / "results" / "all_plots" / "sample_distributions"

config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.05)


print("Obtaining ocean measurements dataset...")
with alive_bar(1) as bar:
    ocean_measurements_data = xr.open_dataset(OCEAN_OBVS)
    raw_measurements_df = ocean_measurements_data.to_dataframe()
    bar()
    t

print("Decoding bytes objects and coercing to floats...")
with alive_bar(1) as bar:
    ocean_measurements_df = CleanData.decode_all_columns(raw_measurements_df)
    bar()
    t

print("Drop erroneous data (Year > 2.008e+03 ; Day > 9.96e+30)...")
with alive_bar(1) as bar:
    ocean_measurements_df = CleanData.drop_erroneous(ocean_measurements_df)
    bar()
    t

print("Adding 'Months' column and saving processed dataset...")
with alive_bar(2) as bar:
    processed_ocean_df = AddMonthsColumn.create_months_column(ocean_measurements_df)
    bar()
    t
    Save.save_to_pkl(
        processed_ocean_df,
        f"{SAVEPATH}/ocean_measurement_data",
        "cleaned_meas_data.pkl",
    )
    bar()
    t


print("Obtaining vectors of ocean measurements' lon, lat & time (mon 1 -> 264)...")
with alive_bar(1) as bar:
    X, Y, T = CreateSamplingMatrix.column_coordinates(processed_ocean_df)
    raw_matrix = CreateSamplingMatrix.raw_matrix(X, Y, T)
    ocean_measurements_matrix = CreateSamplingMatrix.clean_matrix(raw_matrix)
    X, Y, T = CreateSamplingMatrix.matrix_coordinates(ocean_measurements_matrix, type=1)
    bar
    t


print("Obtaining vectors of Darwin cell centre's lon, lat & time (mon 1 -> 264)...")
with alive_bar(1) as bar:
    grid_cell_centres = xr.open_dataset(GRID_CELL)
    x, y, t = CreateSamplingMatrix.matrix_coordinates(grid_cell_centres, type=2)
    bar()
    t


# print("Generating and saving sampling matrices...")
# with alive_bar(3) as bar:
#     I_zero = CreateSamplingMatrix.matrix_of_zeros()
#     I = CreateSamplingMatrix.sampling_matrix(I_zero, X, Y, T, x, y)
#     bar()
#     t
#     # RANDOM SAMPLING MATRIX
#     Ir_zero = np.zeros(shape=(144, 90, 265))
#     Ir = CreateSamplingMatrix.random_matrix(Ir_zero)
#     bar()
#     t
#     CreateSamplingMatrix.save_matrix(
#         I, Ir, "ocean_measurements_matrix", "random_sample_matrix"
#     )
#     bar()
#     t

# print("Generating and saving sample distribution plots...")
# with alive_bar(4) as bar:
#     MatrixPlots.matrix_scatter_plot_3D(
#         I,
#         PLOTPATH,
#         "ocean_measurements_scatterplot",
#         dtype="Observational",
#     )
#     bar()
#     t
#     MatrixPlots.matrix_histogram(
#         I,
#         PLOTPATH,
#         "ocean_measurements_histogram",
#         dtype="Observational",
#     )
#     bar()
#     t
#     MatrixPlots.matrix_scatter_plot_3D(
#         Ir, PLOTPATH, "random_sample_scatterplot", dtype="Random"
#     )
#     bar()
#     t
#     MatrixPlots.matrix_histogram(
#         Ir, PLOTPATH, "random_sample_histogram", dtype="Random"
#     )
#     bar()
#     t
