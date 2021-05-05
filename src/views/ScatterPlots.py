import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import pandas as pd
import os, sys
from pathlib import Path

base_path = Path(os.path.abspath(__file__)).parents[2] / "all_outputs"
INNER_PLOT_SAVE = base_path / "all_plots" / "inner_plots"
SCATTER_SAVE = base_path / "all_plots" / "scatter_plots"


def generate_plots(gams_predictions, darwin_target, summary_stats, savepath):
    plot_max = 2223085
    for i in range(len(summary_stats)):
        plot_inner(
            plot_max,
            (summary_stats["Darwin < cutoff"][i]) * plot_max,
            (summary_stats["GAMs < cutoff"][i]) * plot_max,
            summary_stats["Presence Fraction"][i],
            savepath,
            f"inner_{i}",
        )
    for f_group in gams_predictions:
        for i in range(len(f_group)):
            scatter_plot(
                gams_predictions[f"{f_group}"],
                darwin_target[f"{f_group}"],
                summary_stats["r-squared"][i],
                summary_stats["Means Ratios"][i],
                summary_stats["Medians Ratios"][i],
                f"{INNER_PLOT_SAVE}{savepath}/inner_{i}.png",
                "Darwin v. GAMs",
                "GAMs",
                "Darwin",
                savepath,
                f"{f_group}",
            )


def plot_inner(
    plot_max, darwin_below_cutoff, gams_below_cutoff, frac, savepath, filename
):
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.plot([0, plot_max], [0, plot_max], alpha=0)

    # darwin below cutoff - left red
    ax.add_patch(
        patches.Rectangle(
            (0, 0),  # origin
            darwin_below_cutoff,  # width
            plot_max,  # height
            facecolor="red",
            alpha=0.7,
            fill=True,
        )
    )
    # gams below cutoff - bottom red
    ax.add_patch(
        patches.Rectangle(
            (0, 0), plot_max, gams_below_cutoff, facecolor="red", alpha=0.7, fill=True
        )
    )
    # Both below cutoff
    ax.add_patch(
        patches.Rectangle(
            (0, 0),
            darwin_below_cutoff,
            gams_below_cutoff,
            facecolor="darkred",
            fill=True,
        )
    )
    # Both above cutoff
    ax.add_patch(
        patches.Rectangle(
            (darwin_below_cutoff, gams_below_cutoff),
            plot_max,
            plot_max,
            facecolor="green",
            alpha=1.0,
            fill=True,
        )
    )
    # Green area text
    ax.text(
        0.25 * (darwin_below_cutoff + plot_max),
        0.45 * (gams_below_cutoff + plot_max),
        round(frac, 2),
        fontsize=26,
        fontweight="bold",
        color="white",
    )
    # Overlap rectangle
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
    ax.set_xlim(0, plot_max)
    ax.set_ylim(0, plot_max)
    ax.set_rasterization_zorder(1)  # to retain png quality

    plt.savefig(
        f"{INNER_PLOT_SAVE}{savepath}/{filename}.png",
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
    savepath,
    filename,
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
    plt.hexbin(x, y, gridsize=(60, 60), bins="log", cmap=plt.cm.Greens)
    plt.colorbar(
        orientation="vertical",
        fraction=0.11,
        pad=0.03,
        label="( $\mathregular{mmol\ C/m^3}$ )",
    )

    # Upper left image     CHECK FILE LOCATION
    image = mpimg.imread(inner_plot)

    ax = plt.axes([0.1, 0.65, 0.22, 0.22], frameon=False)
    ax.imshow(image)
    ax.axis("off")

    plt.savefig(
        f"{SCATTER_SAVE}{savepath}/{filename}.pdf",
        format="pdf",
        dpi=1200,
        bbox_inches="tight",
    )
    plt.close(fig)