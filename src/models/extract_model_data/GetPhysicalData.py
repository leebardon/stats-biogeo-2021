import pandas as pd
import numpy as np
import xarray as xr

# generalise to extract at given depth


def get_phys_surface_data(data_path, variable_name):
    surface_arrays = []
    for phys_dataset in data_path.iterdir():
        surface_slice = get_surface_slice(phys_dataset)
        surface_arrays.append(surface_slice)
    matrix = np.stack((surface_arrays))
    return matrix_to_df(matrix, variable_name), matrix


def get_surface_slice(phys_dataset):
    converted_array = binary_to_numpy(phys_dataset)
    converted_array.shape = (22, 90, 144)
    surface_slice = converted_array[0]
    return surface_slice


def binary_to_numpy(phys_dataset):
    converted = np.fromfile(f"{phys_dataset}", dtype=">f4")
    return converted


def matrix_to_df(matrix, variable_name):
    names = ["Month", "Y", "X"]
    index = pd.MultiIndex.from_product(
        [range(series) for series in matrix.shape], names=names
    )
    predictor = pd.DataFrame(
        {f"{variable_name}": matrix.flatten()}, index=index
    ).reset_index()
    predictor["Month"] = predictor["Month"] + 1
    predictor_df = predictor[predictor[f"{variable_name}"] != 0]
    return predictor_df


def get_par_data(par_path, variable_name, years, months, salinity):
    converted = binary_to_numpy(par_path)
    reshaped = converted.reshape(12, 90, 144)
    par_matrix = np.vstack([reshaped] * years)[:months, :, :]
    par = matrix_to_df(par_matrix, "PAR")
    par_df = par.merge(
        salinity, left_on=["Month", "X", "Y"], right_on=["Month", "X", "Y"], how="inner"
    )
    del par_df["SSS"]
    return par_df, par_matrix
