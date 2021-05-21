import os
import numpy as np
import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.gridliner import LATITUDE_FORMATTER

GeoAxes._pcolormesh_patched = Axes.pcolormesh

base_path = Path(os.path.abspath(__file__)).parents[2] / "all_outputs"
MAP_DATA_SAVE = base_path / "map_plotting_data"
MAP_SAVE = base_path / "all_plots" / "maps"


def below_cutoff_to_zero(plankton_dict):
    for group, data in plankton_dict.items():
        data[data < 1.001e-5] = 0
    return plankton_dict


def process_and_plot(predictions_dict, coords, savepath="", maptitle="", mtype=0):
    annual_means = {
        "proko": 0,
        "pico": 0,
        "cocco": 0,
        "diazo": 0,
        "diatom": 0,
        "dino": 0,
        "zoo": 0,
    }

    means_coords = {"lon": 0, "lat": 0}

    for f_group, data in predictions_dict.items():
        group_df = pd.DataFrame(columns=[f"{f_group}", "lon", "lat"])
        group_df[f"{f_group}"] = data
        group_df["lon"], group_df["lat"] = (
            coords["x_deg"].values,
            coords["y_deg"].values,
        )
        means = get_annual_means(group_df, f_group)
        if mtype == 0:
            pivot_to_plot(means, f_group, savepath, maptitle)
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


def pivot_table(means_df, f_group="", savepath="", maptitle="", mtype=0):
    annual_means_pv = means_df.pivot(index="lat", columns="lon")
    annual_means_pv = annual_means_pv.droplevel(0, axis=1)
    annual_means_da = create_datarray_object(
        annual_means_pv, f_group, savepath, maptitle, mtype
    )
    return annual_means_da


def create_datarray_object(annual_means_pv, f_group, savepath, maptitle, mtype):
    annual_means_nan_to_zero = annual_means_pv.fillna(0)
    annual_means_da = xr.DataArray(data=annual_means_nan_to_zero)
    if mtype == 0:
        prep_for_plotting(annual_means_da, f_group, savepath, maptitle)
    else:
        return annual_means_da


def prep_for_plotting(annual_means_da, f_group, savepath, maptitle):
    lat = annual_means_da["lat"].data
    lon = annual_means_da["lon"].data
    biomass = annual_means_da.data
    vmax = np.percentile(biomass, 95)
    plot_map(lon, lat, biomass, vmax, savepath, f_group, maptitle)


def plot_map(lon, lat, biomass, vmax, savepath, filename, maptitle):

    projection = ccrs.PlateCarree(central_longitude=180.0)
    transform = ccrs.PlateCarree()
    cmap = "YlGnBu"
    fc = "lightgray"

    fig = plt.figure(figsize=(7, 4))

    ax = plt.subplot(111, projection=projection)
    ax1 = ax.add_feature(
        cfeature.NaturalEarthFeature(
            "physical", "land", "110m", edgecolor="face", facecolor=fc
        )
    )
    ax1 = ax.pcolormesh(
        lon, lat, biomass, cmap=cmap, transform=transform, vmax=vmax, shading="gouraud"
    )
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
    # ax.scatter(xpoints, ypoints, transform=transform, s=1, color='firebrick')
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
        f"{MAP_SAVE}{savepath}/{filename}.pdf",
        format="pdf",
        dpi=1200,
        bbox_inches="tight",
    )
    plt.close(fig)
