import numpy as np
import os


def decode_single_column(column):
    decoded_rows = []
    for row in column:
        row = row.decode("utf-8")
        row = float(row) if row != "" else np.nan
        decoded_rows.append(row)
    return decoded_rows


def decode_all_columns(ocean_data):
    columns_to_decode = [
        "Phosphate",
        "Nitrite_Nitrate",
        "Temperature",
        "Prochlorococcus",
        "Pico_eukaryotes",
    ]
    for i in columns_to_decode:
        ocean_data[i] = decode_single_column(ocean_data[i])
    return ocean_data


def drop_erroneous(ocean_measurements):
    ocean_measurements = ocean_measurements.query("Year <= 2.008e+03")
    ocean_measurements = ocean_measurements.query("Day <= 9.96e+30")
    return ocean_measurements
