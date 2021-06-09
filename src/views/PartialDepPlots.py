import matplotlib.pyplot as plt


def partial_dependency_plots(path, gams_p, gams_f):
    groups = ["Pro", "Pico", "Cocco", "Diazo", "Diatom", "Dino", "Zoo"]
    for i in range(len(groups)):
        plot_pdp(gams_p[groups[i]], gams_f[groups[i]], groups[i], path)


def plot_pdp(gam_p, gam_f, func_group, path):
    labels = [
        "$\mathregular{PO_4}$",
        "$\mathregular{NO_3}$",
        "Fe",
        "Si",
        "SST",
        "Salinity",
        "PAR",
    ]
    y_label = func_group
    plt.figure()
    fig, axs = plt.subplots(1, 7, figsize=(18, 5))
    fig.tight_layout(pad=2.7)
    for i, ax in enumerate(axs):
        XX1 = gam_p.generate_X_grid(term=i)
        XX2 = gam_f.generate_X_grid(term=i)
        ax.plot(
            XX1[:, i],
            gam_p.partial_dependence(term=i, X=XX1),
            c="r",
            ls="--",
            linewidth=3,
        )
        ax.plot(
            XX1[:, i],
            gam_p.partial_dependence(term=i, X=XX1, width=0.95)[1],
            c="lightgrey",
            ls="-",
            linewidth=1.5,
        )
        ax.plot(XX2[:, i], gam_f.partial_dependence(term=i, X=XX2), linewidth=3)

        if i == 0:
            ax.set_ylabel(y_label, fontsize=20)
        ax.set_xlabel(labels[i], fontsize=12)

    plt.savefig(
        f"{path}/{func_group}.pdf",
        format="pdf",
        dpi=1200,
        bbox_inches="tight",
    )
    plt.close(fig)
