import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D


def matrix_scatter_plot(matrix, path, filename, dtype):
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

    plt.savefig(
        f"{path}/{filename}.pdf",
        format="pdf",
        dpi=1200,
        bbox_inches="tight",
    )
    plt.close(fig)


def matrix_histogram(matrix, path, filename, dtype):
    coordinates = np.where(matrix == 1)
    plt.figure(figsize=(8, 5))
    plt.hist(coordinates[2], 264)
    plt.xlabel("Month", fontsize=11)
    plt.ylabel("Number of Measurements", fontsize=11)
    plt.title(f"{dtype} per Month (1987-2008)", fontsize=14)

    plt.savefig(
        f"{path}/{filename}.pdf",
        format="pdf",
        dpi=1200,
        bbox_inches="tight",
    )
