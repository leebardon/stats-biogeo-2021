import numpy as np
import pandas as pd


def assign_months(year, months_list, ocean_data):
    for i, row in ocean_data.iterrows():
        row = ocean_data.loc[i, "Year"]
        day = ocean_data.loc[i, "Day"]
        if row != year:
            continue
        else:
            if 1.0 >= day < 31.0:
                ocean_data.loc[i, "Month"] = months_list[0]
            elif 31.0 >= day < 60.0:
                ocean_data.loc[i, "Month"] = months_list[1]
            elif 60.0 >= day < 91.0:
                ocean_data.loc[i, "Month"] = months_list[2]
            elif 91.0 >= day < 121.0:
                ocean_data.loc[i, "Month"] = months_list[3]
            elif 121.0 >= day < 152.0:
                ocean_data.loc[i, "Month"] = months_list[4]
            elif 152.0 >= day < 182.0:
                ocean_data.loc[i, "Month"] = months_list[5]
            elif 182.0 >= day < 213.0:
                ocean_data.loc[i, "Month"] = months_list[6]
            elif 213.0 >= day < 244.0:
                ocean_data.loc[i, "Month"] = months_list[7]
            elif 244.0 >= day < 275.0:
                ocean_data.loc[i, "Month"] = months_list[8]
            elif 275.0 >= day < 306.0:
                ocean_data.loc[i, "Month"] = months_list[9]
            elif 306.0 >= day < 336.0:
                ocean_data.loc[i, "Month"] = months_list[10]
            else:
                ocean_data.loc[i, "Month"] = months_list[11]


def years():
    return [i for i in np.arange(1987.0, 2009.0, 1)]


def months():
    return pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])


def create_months_column(ocean_data):
    ocean_data["Month"] = 0
    years_list = years()
    months_list = months()
    for year in years_list:
        assign_months(year, months_list, ocean_data)
        months_list = months_list + 12
    return ocean_data
