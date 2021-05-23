import pandas as pd
import numpy as np
import xarray as xr
import os
from pathlib import Path

base_path = Path(os.path.abspath(__file__)).parents[3] / "data" / "processed"


def get_ecosys_surface_data(ecosys_data_path):
    all_surface_data = []
    month = 1
    for nc_file in ecosys_data_path.iterdir():
        surface_data, col_names = convert_and_extract(nc_file)
        surface_data["Month"] = month
        month += 1
        all_surface_data.append(surface_data)
    final_df = build_combined_surface_df(all_surface_data, col_names)
    return final_df[final_df["pCO2"] != 0]


def convert_and_extract(nc_file):
    col_names = []
    nc_file = xr.open_dataset(nc_file, use_cftime=True)
    df = nc_file.to_dataframe().reset_index()
    col_names.append(df.columns.values.tolist())
    surface_data = get_surface_data(df)
    return surface_data, col_names


def get_surface_data(df):
    surface = df[df["Zmd000022"] == 0]
    surface["Z"] = 0
    return surface


def build_combined_surface_df(all_surface_data, col_names):
    combined_df = pd.DataFrame(
        np.concatenate([df.values for df in all_surface_data]), columns=col_names
    )
    return combined_df


def add_grid_coords(ecosys):
    x_deg, y_deg = get_degrees_columns(ecosys)
    ecosys.rename({"X": "x_deg", "Y": "y_deg"}, axis=1, inplace=True)
    ecosys["X"] = ((2 * x_deg) / 5 + 0.5).astype(int) - 1
    ecosys["Y"] = ((y_deg + 92) / 2).astype(int) - 1
    save_degrees_coords(ecosys)
    return ecosys


def get_degrees_columns(ecosys):
    x_deg = ecosys["X"][:]
    y_deg = ecosys["Y"][:]
    return x_deg, y_deg


def save_degrees_coords(ecosys):
    degrees_coords = ecosys[["x_deg", "y_deg"]]
    degrees_coords.to_pickle(f"{base_path}/model_ocean_data/degrees_coords.pkl")


# METHOD NOT WORKING

# def add_seasons_col(darwin_data):
#     darwin_data["Season"] = None
#     seasons_list = ["winter", "spring", "summer", "autumn"]
#     return assign_seasons(seasons_list, darwin_data)


# def assign_seasons(seasons_list, darwin_data):
#     season_masks = get_season_masks(darwin_data)
#     for i in range(0, len(seasons_list)):
#         _mask = season_masks[i]
#         darwin_data["Season"] = darwin_data["Season"].where(
#             ~_mask, other=seasons_list[i]
#         )


# def get_season_masks(darwin_data):
#     masks = [
#         darwin["Month"][3::12] | darwin["Month"][4::12] | darwin["Month"][5::12],
#         darwin["Month"][6::12] | darwin["Month"][7::12] | darwin["Month"][8::12],
#         darwin["Month"][9::12] | darwin["Month"][10::12] | darwin["Month"][11::12],
#         darwin["Month"][12::12] | darwin["Month"][13::12] | darwin["Month"][14::12],
#     ]
#     ]
#     return masks
