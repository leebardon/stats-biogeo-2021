import cartopy
import os, sys
import numpy as np
import pandas as pd
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib as mp
from pathlib import Path
from netCDF4 import Dataset as NCF
from matplotlib.axes import Axes
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

GeoAxes._pcolormesh_patched = Axes.pcolormesh


from ML_Biogeography_2021.models.generate_plots import Maps


base_path = Path(os.path.abspath(__file__)).parents[2] / "all_outputs"
MAP_DATA_SAVE = base_path / "map_plotting_data"
REL_DIFF_SAVE = base_path / "all_plots" / "relative_diff_maps"


def generate_diff_maps(darwin, gams, coords, savepath, maptitle):
    darwin_means, means_coords = Maps.process_and_plot(darwin, coords, mtype=1)
    gams_means, means_coords = Maps.process_and_plot(gams, coords, mtype=1)
    for f_group, data in darwin_means.items():
        diffs_df = pd.DataFrame(columns=[f"{f_group}_diffs", "lon", "lat"])
        diffs_df[f"{f_group}_diffs"] = (
            gams_means[f"{f_group}"] - darwin_means[f"{f_group}"]
        )
        diffs_df["lon"], diffs_df["lat"] = means_coords["lon"], means_coords["lat"]
        rel_diffs_da = Maps.pivot_table(diffs_df, mtype=1)
        rel_diff_maps(rel_diffs_da, savepath, f_group, maptitle)


def rel_diff_maps(rel_diffs_da, savepath, f_group, maptitle):
    lat = rel_diffs_da["lat"].data
    lon = rel_diffs_da["lon"].data
    biomass = rel_diffs_da.data
    vmin = np.percentile(biomass, 5)
    vmax = np.percentile(biomass, 95)
    plot_diff_map(lon, lat, biomass, vmin, vmax, savepath, f_group, maptitle)


def plot_diff_map(lon, lat, biomass, vmin, vmax, savepath, filename, maptitle):
    extent = [abs(vmin) if abs(vmin) > abs(vmax) else abs(vmax)]
    projection = ccrs.PlateCarree(central_longitude=180.0)
    transform = ccrs.PlateCarree()
    # cmap = "bwr"
    cmap = "Spectral_r"
    #     cmap = 'PiYG'
    #     cmap = 'PuOr'
    fc = "gray"

    fig = plt.figure(figsize=(7, 4))

    ax = plt.subplot(111, projection=projection)
    ax1 = ax.add_feature(
        cfeature.NaturalEarthFeature(
            "physical", "land", "110m", edgecolor="face", facecolor=fc
        )
    )
    ax1 = ax.pcolormesh(
        lon,
        lat,
        biomass * 100,
        cmap=cmap,
        transform=transform,
        vmin=-extent[0] * 100,
        vmax=extent[0] * 100,
        shading="gouraud",
    )
    gl = ax.gridlines(linewidth=0, draw_labels=True)
    gl.yformatter = LATITUDE_FORMATTER
    gl.top_labels, gl.left_labels, gl.right_labels, gl.bottom_labels = (
        False,
        True,
        False,
        False,
    )
    ax.coastlines(linewidth=0.3)
    ax.set_aspect("auto")
    cb = fig.colorbar(
        ax1,
        ax=ax,
        orientation="vertical",
        fraction=0.11,
        pad=0.03,
        label=" Percentage (%) ",
    )
    #     cb.set_label("Mean Difference (%)", labelpad=-1.2, fontsize=11)

    plt.title(maptitle, fontsize=13)
    plt.savefig(
        f"{REL_DIFF_SAVE}{savepath}/{filename}.pdf",
        format="pdf",
        dpi=1200,
        bbox_inches="tight",
    )
    plt.close(fig)
