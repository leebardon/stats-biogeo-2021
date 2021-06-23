import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def correlation_heatmap(colour, path, vmin=None, vmax=None, **data_dicts):
    for filename, df in data_dicts.items():
        if filename == "hmap_diff_r":
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
            sns.set(font_scale=1.4)
            g = sns.heatmap(
                correlations,
                cmap=colour,
                linewidths=1.5,
                annot_kws={"size": 16},
                linecolor="black",
                xticklabels=1,
                yticklabels=1,
                annot=True,
                square=True,
                vmin=vmin,
                vmax=vmax,
            )
            # g.set_xticks(np.arange(7))
            g.set_yticks(np.arange(7) + 0.5)
            g.set_xticklabels(g.get_xmajorticklabels(), fontsize=15.5, ha="center")
            g.set_yticklabels(g.get_ymajorticklabels(), fontsize=15.5, va="center")

            plt.savefig(
                f"{path}/{filename}.pdf",
                format="pdf",
                dpi=1200,
                bbox_inches="tight",
            )
            plt.close(fig)
