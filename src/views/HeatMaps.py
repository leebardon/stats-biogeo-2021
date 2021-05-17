MAP_SAVE = base_path / "all_plots" / "heatmaps"


# not tested, vars need changed
def dcorr_heatmap():
    fig, ax = plt.subplots(figsize=(8, 6))
    cols = ["Proko", "Pico", "Cocco", "Diazo", "Diatom", "Dino", "Zoo"]
    index = ["PO4", "NO3", "Fe", "Si", "SST", "SSS", "PAR"]
    test = pd.DataFrame(
        [
            d["PO4"].values,
            d["NO3"].values,
            d["Fe"].values,
            d["Si"].values,
            d["SST"].values,
            d["SSS"].values,
            d["PAR"].values,
        ],
        columns=cols,
        index=index,
    )
    # plt.yticklabels(index, rotation=90, horizontalalignment='right')
    sns.heatmap(
        test,
        cmap="coolwarm",
        linewidths=1.5,
        linecolor="black",
        annot=True,
        square=True,
    )
    plt.savefig(
        "/Users/leebardon/Desktop/distance_correlation.pdf",
        format="pdf",
        dpi=1200,
        bbox_inches="tight",
    )
