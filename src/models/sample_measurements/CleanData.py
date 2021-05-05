import numpy as np
import os


def decode_single_column(column):
    decoded_rows = []
    for row in column:
        row = row.decode("utf-8")
        row = float(row) if row != "" else np.nan
        decoded_rows.append(row)
    return decoded_rows


def decode_all_columns(columns_to_decode, ocean_data):
    for i in columns_to_decode:
        ocean_data[i] = decode_single_column(ocean_data[i])
    return ocean_data


def save_cleaned_df(ocean_df):
    owd = os.getcwd()
    os.chdir("../all_outputs/ocean_measurement_data")
    path = os.getcwd()
    ocean_df.to_csv(os.path.join(path, r"cleaned_ocean_measurement_data.csv"))
    os.chdir(owd)
