import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path
from random import randint
from src.models.generate_plots import MatrixPlots
from src.models.sample_measurements import (
    CleanData,
    AddMonthsColumn,
    CreateSamplingMatrix,
)

base_path = Path(os.path.abspath(__file__)).parents[2]

OCEAN_OBVS = base_path / "test_data" / "ocean_observations.netcdf"
GRID_CELL = base_path / "test_data" / "grid_igsm.nc"

# Ocean Measurements Dataset
ocean_measurements_data = xr.open_dataset(OCEAN_OBVS)
ocean_measurements_df = ocean_measurements_data.to_dataframe()

# In this instance, columns to decode are known, but could add an interactive
# method to allow user to input on-the-fly for any similar dataset

columns_to_decode = [
    "Phosphate",
    "Nitrite_Nitrate",
    "Temperature",
    "Prochlorococcus",
    "Pico_eukaryotes",
]

# Decode bytes objects and coerce to float
CleanData.decode_all_columns(columns_to_decode, ocean_measurements_df)

# Drop erroneous data (see "Building Sampling Matrix" Jupyter Notebook)
ocean_measurements_df = ocean_measurements_df.query("Year <= 2.008e+03")
ocean_measurements_df = ocean_measurements_df.query("Day <= 9.96e+30")

# Add months column
ocean_measurements_df["Month"] = 0
AddMonthsColumn.create_months_column(ocean_measurements_df)

# Save cleaned dataset
CleanData.save_cleaned_df(ocean_measurements_df)

# Read in a vector of ocean measurements' longitudes, latitudes, and time (month's 1 to 264)
X, Y, T = CreateSamplingMatrix.column_coordinates(ocean_measurements_df)
raw_ocean_matrix = np.vstack([X, Y, T]).T
out_of_bounds = np.where(raw_ocean_matrix > 360)
ocean_measurements_matrix = np.delete(raw_ocean_matrix, out_of_bounds[0], axis=0)
X, Y, T = CreateSamplingMatrix.matrix_coordinates(ocean_measurements_matrix)

# Read in a gridded Darwin matrix (22,90,144)
# Of GRID CELL CENTRE depth, latitudes and longitudes
grid_cell_centres = xr.open_dataset(GRID_CELL_PATH)
x, y, t = CreateSamplingMatrix.grid_matrix(grid_cell_centres)

# Create a 3D matrix of zeros I (size N_x, N_y, N_t)
I_zero = CreateSamplingMatrix.matrix_of_zeros()

# SAMPLING MATRIX from OCEAN MEASUREMENT LOCATIONS
I = CreateSamplingMatrix.sampling_matrix(I_zero, X, Y, T, x, y)
ocean_measurement_locations = np.where(I == 1)

# RANDOM SAMPLING MATRIX
Ir_zero = np.zeros(shape=(144, 90, 265))
Ir = CreateSamplingMatrix.random_matrix(Ir_zero)
random_coords = np.where(Ir == 1)

# Save Binary Sampling Matrices
CreateSamplingMatrix.save_matrix(
    I, Ir, "ocean_measurements_matrix", "random_sample_matrix"
)

# PLOTS
MatrixPlots.matrix_scatter_plot_3D(
    ocean_measurement_locations, "ocean_measurements_scatterplot", dtype="Observational"
)
MatrixPlots.matrix_histogram(
    ocean_measurement_locations, "ocean_measurements_histogram", dtype="Observational"
)
MatrixPlots.matrix_scatter_plot_3D(
    random_coords, "random_sample_scatterplot", dtype="Random"
)
MatrixPlots.matrix_histogram(random_coords, "random_sample_histogram", dtype="Random")
