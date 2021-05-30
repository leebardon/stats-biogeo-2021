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

# NEED TO REVERT TO PREVIOUS - SUMMARY_STATS REQUIRES FULL TABLE
def generate_scatter_plots(predictions, darwin, stats, scattersave, innersave, colours):
    plot_max = len(darwin["Pro"])

    for i in range(len(stats)):
        plot_inner(
            plot_max,
            (stats["Darwin < cutoff"][i]) * plot_max,
            (stats["GAMs < cutoff"][i]) * plot_max,
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
            "Darwin vs. GAMs",
            "GAMs",
            "Darwin",
            scattersave,
            f"{f_group}",
            colours,
        )


def plot_inner(pmax, darwin_below_cutoff, gams_below_cutoff, frac, innersave, filename):
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.plot([0, pmax], [0, pmax], alpha=0)

    # darwin below cutoff - left red
    ax.add_patch(
        patches.Rectangle(
            (0, 0),  # origin
            darwin_below_cutoff,  # width
            pmax,  # height
            facecolor="red",
            alpha=0.7,
            fill=True,
        )
    )
    # gams below cutoff - bottom red
    ax.add_patch(
        patches.Rectangle(
            (0, 0), pmax, gams_below_cutoff, facecolor="red", alpha=0.7, fill=True
        )
    )
    # both below cutoff
    ax.add_patch(
        patches.Rectangle(
            (0, 0),
            darwin_below_cutoff,
            gams_below_cutoff,
            facecolor="darkred",
            fill=True,
        )
    )
    # both above cutoff
    ax.add_patch(
        patches.Rectangle(
            (darwin_below_cutoff, gams_below_cutoff),
            pmax,
            pmax,
            facecolor="green",
            alpha=1.0,
            fill=True,
        )
    )
    # green area text
    ax.text(
        0.25 * (darwin_below_cutoff + pmax),
        0.45 * (gams_below_cutoff + pmax),
        round(frac, 2),
        fontsize=26,
        fontweight="bold",
        color="white",
    )
    # overlap rectangle
    ax.add_patch(
        patches.Rectangle(
            (0, 0),
            darwin_below_cutoff,
            gams_below_cutoff,
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
):

    x = gams_predictions
    y = darwin_target
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

    ax.plot(
        [0, max(gams_predictions)],
        [0, max(darwin_target)],
        c="navy",
        linewidth=2,
    )
    if colours == 1:
        plt.hexbin(x, y, gridsize=(60, 60), bins="log", cmap=plt.cm.Greens)
    else:
        plt.hexbin(x, y, gridsize=(60, 60), bins="log", cmap=plt.cm.Reds)

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
