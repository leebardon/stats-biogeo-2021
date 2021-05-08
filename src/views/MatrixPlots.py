import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import seaborn as sns
import os


def matrix_scatter_plot_3D(matrix, filename, dtype):
    coordinates = np.where(matrix == 1)
    x = coordinates[0]
    y = coordinates[1]
    t = coordinates[2]
    sns.set_style("whitegrid", {"axes.grid": False})
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.grid(False)
    ax.scatter(x, y, t, facecolor=(0, 0, 0, 0), edgecolor="crimson")
    ax.set_ylim(0, 90)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Month")
    ax.set_title(
        f"{dtype} Data Mapped to Grid Cells (1987 - 2008)", fontsize=15, y=1.02
    )

    owd = os.getcwd()
    os.chdir("../all_outputs/all_plots/sample_scatterplots")
    plt.savefig(f"{filename}", format="pdf", dpi=1200)
    os.chdir(owd)


def matrix_histogram(matrix, filename, dtype):

    plt.figure(figsize=(8, 5))
    plt.hist(measurements[2], 264)
    plt.xlabel("Month", fontsize=11)
    plt.ylabel("Number of Measurements", fontsize=11)
    plt.title(f"{dtype} per Month (1987-2008)", fontsize=14)

    owd = os.getcwd()
    os.chdir("../all_outputs/all_plots/sample_histograms")
    filepath = os.getcwd()
    plt.savefig(f"{filepath}/{filename}", format="pdf", dpi=1200)
    os.chdir(owd)
