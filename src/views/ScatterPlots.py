import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg

# from mpl_toolkits.axes_grid1.inset_locator import inset_axes
# import pandas as pd
# import os, sys
# from pathlib import Path

# base_path = Path(os.path.abspath(__file__)).parents[2] / "all_outputs"
# INNER_PLOT_SAVE = base_path / "all_plots" / "inner_plots"
# SCATTER_SAVE = base_path / "all_plots" / "scatter_plots"


def generate_scatter_plots(
    predictions, darwin, stats, scattersave, innersave, colours, settings
):
    plot_max = len(darwin["Pro"])
    for i in range(len(stats)):
        plot_inner(
            plot_max,
            (stats["Darwin < cutoff"][i]),
            (stats["GAMs < cutoff"][i]),
            stats["Both > cutoff"][i],
            innersave,
            f"inner_{i}",
        )

    f_groups = {
        0: "Pro",
        1: "Pico",
        2: "Cocco",
        3: "Diazo",
        4: "Diatom",
        5: "Dino",
        6: "Zoo",
    }
    for j, f_group in f_groups.items():
        scatter_plot(
            predictions[f"{f_group}"],
            darwin[f"{f_group}"],
            stats["r-squared"][j],
            stats["Means Ratios"][j],
            stats["Medians Ratios"][j],
            f"{innersave}/inner_{j}.png",
            "GAMs vs. Darwin",
            "Darwin",
            "GAMs",
            scattersave,
            f"{f_group}",
            colours,
            settings[f_group][0],
            settings[f_group][1],
        )


def plot_inner(pmax, darwin_below_cut, gams_below_cut, frac, innersave, filename):
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.plot([0, pmax], [0, pmax], alpha=0)

    # gams below cutoff - left red
    ax.add_patch(
        patches.Rectangle(
            (0, 0),  # origin
            gams_below_cut,  # width
            pmax,  # height
            facecolor="red",
            alpha=0.7,
            fill=True,
        )
    )
    # darwin below cutoff - bottom red
    ax.add_patch(
        patches.Rectangle(
            (0, 0), pmax, darwin_below_cut, facecolor="red", alpha=0.7, fill=True
        )
    )
    # both below cutoff
    ax.add_patch(
        patches.Rectangle(
            (0, 0),
            gams_below_cut,
            darwin_below_cut,
            facecolor="darkred",
            fill=True,
        )
    )
    # both above cutoff
    ax.add_patch(
        patches.Rectangle(
            (gams_below_cut, darwin_below_cut),
            pmax,
            pmax,
            facecolor="green",
            alpha=1.0,
            fill=True,
        )
    )
    # green area text
    ax.text(
        0.25 * (darwin_below_cut + pmax),
        0.45 * (gams_below_cut + pmax),
        round((frac/pmax), 2),
        fontsize=26,
        fontweight="bold",
        color="white",
    )
    # overlap rectangle
    ax.add_patch(
        patches.Rectangle(
            (0, 0),
            gams_below_cut,
            darwin_below_cut,
            facecolor="darkred",
            fill=True,
        )
    )
    plt.tick_params(
        bottom=False, top=False, left=False, labelbottom=False, labelleft=False
    )
    ax.set_xlim(0, pmax)
    ax.set_ylim(0, pmax)
    ax.set_rasterization_zorder(1)  # to retain png quality

    plt.savefig(
        f"{innersave}/{filename}.png",
        format="png",
        dpi=1200,
        bbox_inches="tight",
    )
    plt.close(fig)


def scatter_plot(
    gams_predictions,
    darwin_target,
    r,
    means_ratio,
    medians_ratio,
    inner_plot,
    title,
    xlabel,
    ylabel,
    scattersave,
    filename,
    colours,
    xlim,
    ylim,
):

    x = darwin_target
    y = gams_predictions
    fig, ax = plt.subplots(figsize=(6, 4))

    # Lower right box
    textstr = "\n".join(
        (
            r"$R^2$" + " = {}".format(round(r, 2)),
            r"$\bar{X}_{me}$" + " = {}".format(round(means_ratio, 2)),
            r"$\tilde{X}_{md}$" + " = {}".format(round(medians_ratio, 2)),
        )
    )
    props = dict(
        boxstyle="round", facecolor="honeydew", edgecolor="darkorange", alpha=0.6
    )
    ax.text(
        0.74,
        0.28,
        textstr,
        transform=ax.transAxes,
        fontsize=12,
        verticalalignment="top",
        bbox=props,
    )

    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=15)

    if colours == 1:
        ax.plot(x, x, c="navy", linewidth=2)
        plt.hexbin(x, y, gridsize=(60, 60), bins="log", cmap=plt.cm.Greens)
    else:
        ax.plot(x, x, c="navy", linewidth=2)
        plt.hexbin(x, y, gridsize=(60, 60), bins="log", cmap=plt.cm.Reds)

    plt.xlim(0, xlim)
    plt.ylim(0, ylim)

    plt.colorbar(
        orientation="vertical",
        fraction=0.11,
        pad=0.03,
        label="$log_{10}(N)$",
    )

    # Upper left image     CHECK FILE LOCATION
    image = mpimg.imread(inner_plot)

    ax = plt.axes([0.1, 0.65, 0.22, 0.22], frameon=False)
    ax.imshow(image)
    ax.axis("off")

    plt.savefig(
        f"{scattersave}/{filename}.pdf",
        format="pdf",
        dpi=1200,
        bbox_inches="tight",
    )
    plt.close(fig)


class ScatterSettings:
    def __init__(self):
        # [xlim, ylim]
        self.present = {
            "Pro": [0.74, 0.74],
            "Pico": [0.58, 0.58],
            "Cocco": [1.1, 1.1],
            "Diazo": [0.3, 0.3],
            "Diatom": [3, 3],
            "Dino": [1.52, 1.52],
            "Zoo": [8.68, 8.68],
        }
        self.future = {
            "Pro": [0.71, 0.71],
            "Pico": [0.6, 0.6],
            "Cocco": [1.1, 1.1],
            "Diazo": [0.3, 0.3],
            "Diatom": [2.94, 2.94],
            "Dino": [1.42, 1.42],
            "Zoo": [8.36, 8.36],
        }
