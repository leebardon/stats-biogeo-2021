import matplotlib.pyplot as plt


def partial_dependency_plots(predictors, plankton_gams_dict, SAVE_PATH, pathnum):
    for group_name, gam in plankton_gams_dict.items():
        plot_pdp(predictors, gam, group_name, SAVE_PATH, pathnum)


def plot_pdp(predictors, gam, group_name, SAVE_PATH, pathnum):
    y_label = "Biomass ($\mathregular{mmol\ C/m^3}$)"
    title = "Partial Dependency of Biomass to Predictors (1987-2008)"
    labels = [
        "$\mathregular{NO_3}$",
        "$\mathregular{PO_4}$",
        "Si",
        "Fe",
        "SSS",
        "SST",
        "PAR",
    ]
    filename = f"{group_name}_pdp.pdf"
    fig, axs = plt.subplots(1, 7, figsize=(18, 5))
    fig.tight_layout(pad=3.4)

    for i, ax in enumerate(axs):
        XX = gam.generate_X_grid(term=i)
        ax.plot(XX[:, i], gam.partial_dependence(term=i, X=XX))
        ax.plot(
            XX[:, i], gam.partial_dependence(term=i, X=XX, width=0.95)[1], c="r", ls="-"
        )
        if i == 0:
            ax.set_ylabel(y_label, fontsize=12)
        ax.set_xlabel(labels[i], fontsize=12)
        plt.suptitle(title, fontsize=18, y=1.1)
        if pathnum == 1:
            plt.savefig(
                f"{SAVE_PATH}/partial_dep_plots/from_measurements/{filename}",
                format="pdf",
                dpi=1200,
            )
        else:
            plt.savefig(
                f"{SAVE_PATH}/partial_dep_plots/from_random/{filename}",
                format="pdf",
                dpi=1200,
            )
