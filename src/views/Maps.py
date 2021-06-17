import os
import numpy as np
import pandas as pd
import pickle
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from src.models import Save
from pathlib import Path
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.gridliner import LATITUDE_FORMATTER

GeoAxes._pcolormesh_patched = Axes.pcolormesh

basepath = Path(os.path.abspath(__file__)).parents[2]
MAPDATA = basepath / "data" / "processed"
# COORDS = basepath / "data" / "processed" / "model_ocean_data"


def get_dataset(path):
    with open(f"{path}", "rb") as handle:
        dataset = pickle.load(handle)
    return dataset


def get_coords(COORDS):
    return get_dataset(f"{COORDS}/degrees_coords.pkl")


def get_sample_coords():
    data = get_dataset(f"{MAPDATA}/model_ocean_data/samp_coords.pkl")
    return data["x_deg"], data["y_deg"]


def get_inner(basepath, *paths):
    datasets = []
    for path in paths:
        datasets.append(get_dataset(f"{basepath}/{path}"))
    return [ds for ds in datasets]


def below_cutoff_to_cutoff(plankton_dict):
    for group, data in plankton_dict.items():
        data[data < 1.001e-5] = 1.001e-5
    return plankton_dict


def process_and_plot(data_dict, coords, filepath="", maptitle="", mtype=0):

    annual_means = {
        "Pro": 0,
        "Pico": 0,
        "Cocco": 0,
        "Diazo": 0,
        "Diatom": 0,
        "Dino": 0,
        "Zoo": 0,
    }
    means_coords = {"lon": 0, "lat": 0}

    for f_group, data in data_dict.items():
        group_df = pd.DataFrame(columns=[f"{f_group}", "lon", "lat"])
        group_df[f"{f_group}"] = data
        group_df["lon"], group_df["lat"] = (
            coords["x_deg"].values,
            coords["y_deg"].values,
        )
        means = get_annual_means(group_df, f_group)
        if mtype == 0:
            pivot_table(means, f_group, filepath, maptitle)
        else:
            annual_means[f"{f_group}"] = means[f"{f_group} annual means"].values
            means_coords["lon"] = means["lon"].values
            means_coords["lat"] = means["lat"].values

    return annual_means, means_coords


def get_annual_means(group_df, f_group):
    annual_means = (
        group_df.groupby(["lon", "lat"])[f"{f_group}"]
        .mean()
        .to_frame(name=f"{f_group} annual means")
        .reset_index()
    )
    return annual_means


def pivot_table(means_df, f_group="", filepath="", maptitle="", mtype=0):
    annual_means_pv = means_df.pivot(index="lat", columns="lon")
    annual_means_pv = annual_means_pv.droplevel(0, axis=1)
    annual_means_da = create_datarray_object(
        annual_means_pv, f_group, filepath, maptitle, mtype
    )
    return annual_means_da


def create_datarray_object(annual_means_pv, f_group, filepath, maptitle, mtype):
    annual_means_nan_to_zero = annual_means_pv.fillna(0)
    annual_means_da = xr.DataArray(data=annual_means_nan_to_zero)
    if mtype == 0:
        prep_for_plotting(annual_means_da, f_group, filepath, maptitle)
    else:
        return annual_means_da


def prep_for_plotting(annual_means_da, f_group, filepath, maptitle):
    lat = annual_means_da["lat"].data
    lon = annual_means_da["lon"].data
    biomass = annual_means_da.data
    vmax = np.percentile(biomass, 95)
    plot_map(lon, lat, biomass, vmax, filepath, f_group, maptitle)


def plot_map(lon, lat, biomass, vmax, path, f_group, maptitle):
    # set projection and colours
    projection = ccrs.PlateCarree(central_longitude=180.0)
    transform = ccrs.PlateCarree()
    cmap = "YlGnBu"
    fc = "lightgray"

    # generate fig and axes
    fig = plt.figure(figsize=(7, 4))
    ax = plt.subplot(111, projection=projection)

    # add map details
    ax1 = ax.add_feature(
        cfeature.NaturalEarthFeature(
            "physical", "land", "110m", edgecolor="face", facecolor=fc
        )
    )

    # plot data
    ax1 = ax.pcolormesh(
        lon, lat, biomass, cmap=cmap, transform=transform, vmax=vmax, shading="gouraud"
    )

    # format gridlines, coastlines, and labelling
    gl = ax.gridlines(linewidth=0, draw_labels=True)
    gl.top_labels, gl.left_labels, gl.right_labels, gl.bottom_labels = (
        False,
        True,
        False,
        False,
    )
    gl.yformatter = LATITUDE_FORMATTER
    ax.coastlines(linewidth=0.3)
    ax.set_aspect("auto")

    # add location of measurements
    if f_group == "Cocco" and path.endswith("present/darwin"):
        sample_x, sample_y = get_sample_coords()
        ax.scatter(sample_x, sample_y, transform=transform, s=0.8, color="firebrick")

    fig.colorbar(
        ax1,
        ax=ax,
        orientation="vertical",
        fraction=0.11,
        pad=0.03,
        label=" $\mathregular{mmol\ C/m^3}$ -- 95th pct ",
    )
    plt.title(maptitle, fontsize=13)

    plt.savefig(
        f"{path}/{f_group}_map.pdf",
        format="pdf",
        dpi=1200,
        bbox_inches="tight",
    )
    plt.close(fig)
