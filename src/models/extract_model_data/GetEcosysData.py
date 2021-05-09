import pandas as pd
import numpy as np
import xarray as xr

base_path = Path(os.path.abspath(__file__)).parents[2] / "all_outputs"


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
    ecosys["X"] = ((2 * x_deg) / 5 + 0.5).astype(int)
    ecosys["Y"] = ((y_deg + 92) / 2).astype(int)
    save_degrees_coords(ecosys)
    return ecosys


def get_degrees_columns(ecosys):
    x_deg = ecosys["X"][:]
    y_deg = ecosys["Y"][:]
    return x_deg, y_deg


def save_degrees_coords(ecosys):
    degrees_coords = ecosys[["x_deg", "y_deg"]]
    degrees_coords.to_pickle(f"{base_path}/model_whole_ocean_data/degrees_coords.pkl")
