import numpy as np
import os
from random import randint


def column_coordinates(ocean_df):
    X = ocean_df["Longitude"][:]
    Y = ocean_df["Latitude"][:]
    T = ocean_df["Month"][:]
    return X, Y, T


def matrix_coordinates(matrix):
    X = matrix[:, 0]
    Y = matrix[:, 1]
    T = matrix[:, 2]
    return X, Y, T


def grid_matrix(grid):
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


def random_matrix(Ir):
    for _ in range(10000):
        rx = randint(1, 143)
        ry = randint(1, 89)
        rt = randint(1, 264)
        Ir[rx, ry, rt] = 1
    return Ir


def save_matrix(ocean_matrix, random_matrix, filename1, filename2):
    owd = os.getcwd()
    os.chdir("../all_outputs/sampling_matrices")
    path = os.getcwd()
    np.save(f"{path}/{filename1}", ocean_matrix)
    np.save(f"{path}/{filename2}", random_matrix)
    os.chdir(owd)
