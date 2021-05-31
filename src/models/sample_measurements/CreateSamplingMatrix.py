import numpy as np
import os
from random import randint


def column_coordinates(ocean_df):
    X = ocean_df["Longitude"][:]
    Y = ocean_df["Latitude"][:]
    T = ocean_df["Month"][:]
    return X, Y, T


def raw_matrix(X, Y, T):
    return np.vstack([X, Y, T]).T


def clean_matrix(raw_ocean_matrix):
    out_of_bounds = np.where(raw_ocean_matrix > 360)
    return np.delete(raw_ocean_matrix, out_of_bounds[0], axis=0)


def matrix_coordinates(matrix, type):
    if type == 1:
        lon = matrix[:, 0]
        lat = matrix[:, 1]
        months = matrix[:, 2]
    else:
        lon = matrix["X"].data
        lat = matrix["Y"].data
        months = np.arange(1, 265, 1)

    return lon, lat, months


def darwin_matrix_ccordinates(grid):
    x = grid["X"].data
    y = grid["Y"].data
    t = np.arange(1, 265, 1)
    return x, y, t


def matrix_of_zeros():
    return np.zeros(shape=(144, 90, 265))


def sampling_matrix(I, X, Y, T, x, y):
    for j in range(0, 58812):
        ix = abs(X[j] - x).argmin()
        iy = abs(Y[j] - y).argmin()
        it = int(T[j])
        I[ix, iy, it] = 1
    return I


def random_matrix(SEED, num):
    Ir = np.zeros(shape=(144, 90, 265))
    rng = np.random.default_rng(SEED)
    for _ in range(num):
        rx = rng.integers(low=0, high=144)
        ry = rng.integers(low=0, high=90)
        rt = rng.integers(low=0, high=264)
        Ir[rx, ry, rt] = 1
    return Ir
