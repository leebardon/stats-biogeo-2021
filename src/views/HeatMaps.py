import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def correlation_heatmap(colour, path, vmin=None, vmax=None, **data_dicts):
    for filename, df in data_dicts.items():
        fig, ax = plt.subplots(figsize=(8, 6))
        cols = ["Pro", "Pico", "Cocco", "Diazo", "Diatom", "Dino", "Zoo"]
        index = ["PO4", "NO3", "Fe", "Si", "SST", "SSS", "PAR"]
        correlations = pd.DataFrame(
            [
                df["PO4"].values,
                df["NO3"].values,
                df["Fe"].values,
                df["Si"].values,
                df["SST"].values,
                df["SSS"].values,
                df["PAR"].values,
            ],
            columns=cols,
            index=index,
        )
        # plt.yticklabels(index, rotation=90, horizontalalignment='right')
        sns.heatmap(
            correlations,
            cmap=colour,
            linewidths=1.5,
            annot_kws={"size": 16},
            linecolor="black",
            annot=True,
            square=True,
            vmin=vmin,
            vmax=vmax,
        )
        plt.savefig(
            f"{path}/{filename}.pdf",
            format="pdf",
            dpi=1200,
            bbox_inches="tight",
        )
        plt.close(fig)
