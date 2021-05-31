import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import xarray as xr
import numpy as np
import time
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.views import MatrixPlots
from src.models import Save
from src.models.sample_measurements import (
    CleanData,
    AddColumns,
    CreateSamplingMatrix,
)

base_path = Path(os.path.abspath(__file__)).parents[2]
OCEAN_OBVS = base_path / "data" / "raw" / "ocean_observations.netcdf"
GRID_CELL = base_path / "data" / "raw" / "grid_igsm.nc"
SAVEPATH = base_path / "data" / "processed"
PLOTPATH = base_path / "results" / "all_plots" / "sample_distributions"
SEED = 2021_1
SEED2 = 2021_2
SEED3 = 2021_3

# CREATE OUTPUT FILES

config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(1)


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

print("Adding 'Months' and 'Seasons' columns and saving processed dataset...")
with alive_bar(2) as bar:
    processed_ocean_df = AddColumns.create_months_column(ocean_measurements_df)
    processed_ocean_df = AddColumns.create_seasons_column(ocean_measurements_df)
    bar()
    t

    Save.save_to_pkl(
        f"{SAVEPATH}/ocean_measurement_data",
        **{"cleaned_meas_data.pkl": processed_ocean_df},
    )
    bar()
    t


print("Obtaining vectors of ocean measurements' lon, lat & time (mon 1 -> 264)...")
with alive_bar(1) as bar:
    X, Y, T = CreateSamplingMatrix.column_coordinates(processed_ocean_df)
    raw_matrix = CreateSamplingMatrix.raw_matrix(X, Y, T)
    ocean_measurements_matrix = CreateSamplingMatrix.clean_matrix(raw_matrix)
    X, Y, T = CreateSamplingMatrix.matrix_coordinates(ocean_measurements_matrix, type=1)
    bar()
    t


print("Obtaining vectors of Darwin cell centre's lon, lat & time (mon 1 -> 264)...")
with alive_bar(1) as bar:
    grid_cell_centres = xr.open_dataset(GRID_CELL)
    x, y, t = CreateSamplingMatrix.matrix_coordinates(grid_cell_centres, type=2)
    bar()
    t


print("Generating and saving sampling matrices...")
with alive_bar(3) as bar:
    I_zeros = CreateSamplingMatrix.matrix_of_zeros()
    I = CreateSamplingMatrix.sampling_matrix(I_zeros, X, Y, T, x, y)
    bar()
    t
    Ir = CreateSamplingMatrix.random_matrix(SEED, 10000)
    Ir2 = CreateSamplingMatrix.random_matrix(SEED2, 20000)
    Ir3 = CreateSamplingMatrix.random_matrix(SEED3, 40000)
    bar()
    t
    Save.save_matrix(
        f"{SAVEPATH}/sampling_matrices",
        **{
            "ocean_sample_matrix.npy": I,
            "random_sample_matrix.npy": Ir,
            "random_matrix_2.npy": Ir2,
            "random_matrix_3.npy": Ir3,
        },
    )
    bar()
    t

print("Generating and saving sample distribution plots...")
with alive_bar(4) as bar:
    MatrixPlots.matrix_scatter_plot(
        I,
        PLOTPATH,
        "ocean_measurements_scatterplot",
        dtype="Observational",
    )
    bar()
    t

    MatrixPlots.matrix_histogram(
        I,
        PLOTPATH,
        "ocean_measurements_histogram",
        dtype="Observational",
    )
    bar()
    t

    MatrixPlots.matrix_scatter_plot(
        Ir, PLOTPATH, "random_sample_scatterplot", dtype="Random"
    )
    bar()
    t

    MatrixPlots.matrix_histogram(
        Ir, PLOTPATH, "random_sample_histogram", dtype="Random"
    )
    bar()
    t
