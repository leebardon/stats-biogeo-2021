import matplotlib.pyplot as plt


def partial_dependency_plots(predictors, plankton_gams_dict, SAVE_PATH):
    for group_name, gam in plankton_gams_dict.items():
        plot_pdp(predictors, gam, group_name, SAVE_PATH)


def plot_pdp(X1, X2, gam1, gam2, filename):
    y_label = "Biomass ($\mathregular{mmol\ C/m^3}$)"
    title = "Partial Dependency of Biomass to Predictors"
    labels = [
        "$\mathregular{PO_4}$",
        "$\mathregular{NO_3}$",
        "Fe",
        "Si",
        "SST",
        "SSS",
        "PAR",
    ]
    filename = f"{group_name}_pdp.pdf"
    fig, axs = plt.subplots(1, 7, figsize=(18, 5))
    fig.tight_layout(pad=3.4)

    for i, ax in enumerate(axs):
        XX1 = gam1.generate_X_grid(term=i)
        XX2 = gam2.generate_X_grid(term=i)
        ax.plot(
            XX1[:, i],
            gam1.partial_dependence(term=i, X=XX1),
            c="red",
            ls="--",
            linewidth=3,
        )
        ax.plot(
            XX1[:, i],
            gam1.partial_dependence(term=i, X=XX1, width=0.95)[1],
            c="lightgrey",
            ls="-",
            linewidth=1.5,
        )
        ax.plot(XX2[:, i], gam2.partial_dependence(term=i, X=XX2), linewidth=3)

        if i == 0:
            ax.set_ylabel(y_label, fontsize=12)

        ax.set_xlabel(labels[i], fontsize=12)
        plt.suptitle(title, fontsize=18, y=1.1)

        plt.savefig(
            f"{SAVE_PATH}/{filename}",
            format="pdf",
            dpi=1200,
        )
