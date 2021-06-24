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


from src.views import Maps


base_path = Path(os.path.abspath(__file__)).parents[2] / "all_outputs"
# MAP_DATA_SAVE = base_path / "map_plotting_data"
# REL_DIFF_SAVE = base_path / "all_plots" / "relative_diff_maps"


def generate_diff_maps(darwin, gams, coords, savepath, maptitle, settings):
    darwin_means, means_coords = Maps.process_and_plot(darwin, coords, mtype=1)
    gams_means, means_coords = Maps.process_and_plot(gams, coords, mtype=1)

    for f_group, data in darwin_means.items():
        diffs_df = pd.DataFrame(columns=[f"{f_group}_diffs", "lon", "lat"])
        diffs_df[f"{f_group}_diffs"] = (
            gams_means[f"{f_group}"] - darwin_means[f"{f_group}"]
        )
        diffs_df["lon"], diffs_df["lat"] = means_coords["lon"], means_coords["lat"]
        rel_diffs_da = Maps.pivot_table(diffs_df, mtype=1)
        rel_diff_maps(rel_diffs_da, savepath, f_group, maptitle, settings)


def rel_diff_maps(rel_diffs_da, savepath, f_group, maptitle, settings):
    lat = rel_diffs_da["lat"].data
    lon = rel_diffs_da["lon"].data
    biomass = rel_diffs_da.data
    # vmin = np.percentile(biomass, 5)
    # vmax = np.percentile(biomass, 95)
    vmin = settings[f_group][0]
    vmax = settings[f_group][1]
    plot_diff_map(lon, lat, biomass, vmin, vmax, savepath, f_group, maptitle)


def plot_diff_map(lon, lat, biomass, vmin, vmax, savepath, filename, maptitle):
    # extent = [abs(vmin) if abs(vmin) > abs(vmax) else abs(vmax)]
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
        # vmin=-extent[0] * 100,
        # vmax=extent[0] * 100,
        vmin=vmin,
        vmax=vmax,
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
        f"{savepath}/{filename}.pdf",
        format="pdf",
        dpi=1200,
        bbox_inches="tight",
    )
    plt.close(fig)


class DiffMapSettings:
    def __init__(self):
        # [scaling present and future map to whichever has the wider range, for direct comparison]

        self.obvs = {
            "Pro": [-17.0, 17.0],
            "Pico": [-15.5, 15.5],
            "Cocco": [-12.0, 12.0],
            "Diazo": [-8.5, 8.5],
            "Diatom": [-42.0, 42.0],
            "Dino": [-17.0, 17.0],
            "Zoo": [-125.0, 125.0],
        }
        self.rand = {
            "Pro": [-8.5, 8.5],
            "Pico": [-7.5, 7.5],
            "Cocco": [-15.0, 15.0],
            "Diazo": [-7.0, 7.0],
            "Diatom": [-25.0, 25.0],
            "Dino": [-15.0, 15.0],
            "Zoo": [-85.0, 85.0],
        }

class DiffMapSettingsTest:
    def __init__(self):
        # [scaling present and future map to whichever has the wider range, for direct comparison]

        self.obvs = {
            "Pro": [-20.0, 20.0],
            "Pico": [-15.5, 15.5],
            "Cocco": [-20.0, 20.0],
            "Diazo": [-10, 10],
            "Diatom": [-42.0, 42.0],
            "Dino": [-25.0, 25.0],
            "Zoo": [-150.0, 150.0],
        }
        self.rand = {
            "Pro": [-8.5, 8.5],
            "Pico": [-7.5, 7.5],
            "Cocco": [-15.0, 15.0],
            "Diazo": [-7.0, 7.0],
            "Diatom": [-25.0, 25.0],
            "Dino": [-15.0, 15.0],
            "Zoo": [-85.0, 85.0],
        }