import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

FN_GROUP = ["Prok", "Pico", "Cocco", "Diaz", "Diatom", "Mixo", "Zoo"]


def generate_barplot(path, summ, summ_f, summ_r, summ_rf):
    summary_datasets = [summ, summ_f, summ_r, summ_rf]
    rsquareds = get_vars("r-squared", *summary_datasets)
    balanced_accs = get_vars("Balanced Acc.", *summary_datasets)
    means_ratios = get_vars("Means Ratios", *summary_datasets)
    barplot(path, rsquareds, balanced_accs, means_ratios)


def get_vars(var_type, *summary_datasets):
    return [s[var_type].values for s in summary_datasets]


def barplot(path, rsqs, b_accs, m_rats):

    legend_elements = [
        Patch(facecolor="darkgreen", alpha=0.7, label="Historical"),
        Patch(facecolor="darkred", alpha=0.7, label="Future"),
        Patch(facecolor="black", alpha=0.6, label="Observed"),
        Patch(facecolor="None", edgecolor="black", lw=1.8, alpha=0.9, label="Random"),
    ]

    # set barwidth
    bw = 0.42

    # Set position of bar on X axis
    r1 = np.arange(len(rsqs[0]))
    r2 = [x + bw for x in r1]

    # generate axes and set font
    fig, axes = plt.subplots(nrows=3, sharex=True, sharey=False, figsize=(8, 7))
    plt.rcParams.update({"font.family": "serif"})

    # plot axis 1
    ax1 = plt.subplot(311)
    ax1.bar(
        r2,
        m_rats[0],
        color="darkgreen",
        width=-bw / 1.3,
        edgecolor="white",
        align="edge",
        alpha=0.6,
    )
    ax1.bar(
        r2,
        m_rats[1],
        color="darkred",
        width=bw / 1.3,
        edgecolor="white",
        align="edge",
        alpha=0.6,
    )
    ax1.bar(
        r2,
        m_rats[2],
        color="None",
        width=-bw,
        edgecolor="green",
        linewidth=2.2,
        align="edge",
    )
    ax1.bar(
        r2,
        m_rats[3],
        color="None",
        width=bw,
        edgecolor="brown",
        linewidth=2.2,
        align="edge",
    )
    ax1.set_ylim([0, 0.55])
    ax1.set_ylabel("Mean Rel. Diff.", fontsize=13, labelpad=10)
    leg = ax1.legend(
        handles=legend_elements, loc="upper left", fontsize=9, ncol=2, prop={"size": 11}
    )
    ax1.set_xticks([])

    # add legend
    for patch in leg.get_patches():
        patch.set_height(12)
        patch.set_y(-3)

    # plot axis 2
    ax2 = plt.subplot(312)
    ax2.bar(
        r2,
        b_accs[0],
        color="darkgreen",
        width=-bw / 1.3,
        edgecolor="white",
        align="edge",
        alpha=0.6,
    )
    ax2.bar(
        r2,
        b_accs[1],
        color="darkred",
        width=bw / 1.3,
        edgecolor="white",
        align="edge",
        alpha=0.6,
    )
    ax2.bar(
        r2,
        b_accs[2],
        color="None",
        width=-bw,
        edgecolor="green",
        linewidth=2.2,
        align="edge",
    )
    ax2.bar(
        r2,
        b_accs[3],
        color="None",
        width=bw,
        edgecolor="brown",
        linewidth=2.2,
        align="edge",
    )
    ax2.set_ylim([0.45, 0.75])
    ax2.set_ylabel("Bal. Accuracy", fontsize=13, labelpad=10)
    ax2.set_xticks([])

    # plot axis 3
    ax3 = plt.subplot(313)
    ax3.bar(
        r2,
        rsqs[0],
        color="darkgreen",
        width=-bw / 1.3,
        edgecolor="white",
        align="edge",
        alpha=0.6,
    )
    ax3.bar(
        r2,
        rsqs[1],
        color="darkred",
        width=bw / 1.3,
        edgecolor="white",
        align="edge",
        alpha=0.6,
    )
    ax3.bar(
        r2,
        rsqs[2],
        color="None",
        width=-bw,
        edgecolor="green",
        linewidth=2.2,
        align="edge",
    )
    ax3.bar(
        r2,
        rsqs[3],
        color="None",
        width=bw,
        edgecolor="brown",
        linewidth=2.2,
        align="edge",
    )
    ax3.set_ylabel(r"$R^2$", fontsize=16, labelpad=8)
    ax3.set_ylim([-0.23, 1])

    # Add xticks in the middle of the group bars
    plt.xticks(
        [r + bw for r in range(len(rsqs[0]))],
        ["Pro", "Pico", "Cocco", "Diazo", "Diatom", "Dino", "Zoo"],
        fontsize=13,
    )

    plt.tight_layout(pad=2)
    plt.locator_params(axis="y", nbins=3)
    plt.savefig(
        f"{path}/Figure_2.pdf",
        format="pdf",
        dpi=1200,
        bbox_inches="tight",
    )


class AxisSettings:
    def __init__(self, bw):
        self.c = None
        self.w = None
        self.ec = None
        self.lw = 0
        self.ali = "edge"
        self.alp = None
        self.bw = bw

    @property
    def type1(self):
        self.c = "darkgreen"
        self.w = -(self.bw / 1.3)
        self.ec = "white"
        self.alp = 0.6
        return self.c, self.w, self.ec, self.ali, self.alp
