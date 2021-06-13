import numpy as np
from src.models import Utils

log = Utils.setup_logger("syslog")
scilog = Utils.setup_logger("scilog_ocean_meas")


def decode_single_column(column):
    decoded_rows = []
    for row in column:
        row = row.decode("utf-8")
        row = float(row) if row != "" else np.nan
        decoded_rows.append(row)
    return decoded_rows


def decode_all_columns(ocean_data):
    # scilog.info("Decoding binary ocean data cols")
    columns_to_decode = [
        "Phosphate",
        "Nitrite_Nitrate",
        "Temperature",
        "Prochlorococcus",
        "Pico_eukaryotes",
    ]
    for i in columns_to_decode:
        ocean_data[i] = decode_single_column(ocean_data[i])

    # scilog.info(f"Decoded: {ocean_data.head()}")
    return ocean_data


def drop_erroneous(ocean_meas):
    # scilog.info("Removing Year > 2.008e+03, Day > 9.96e+30")
    ocean_meas = ocean_meas.query("Year <= 2.008e+03")
    ocean_meas = ocean_meas.query("Day <= 9.96e+30")
    # scilog.info("Max Year -> {ocean_meas[Year].max()}")
    return ocean_meas
