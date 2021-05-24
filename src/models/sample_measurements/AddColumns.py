import numpy as np
import pandas as pd


def years():
    return [i for i in np.arange(1987.0, 2009.0, 1)]


def months():
    return pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])


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


def create_months_column(ocean_data):
    ocean_data["Month"] = 0
    years_list = years()
    months_list = months()
    for year in years_list:
        assign_months(year, months_list, ocean_data)
        months_list += 12
    return ocean_data


# NEW VECTORISED MASKING METHOD FOR MONTH AND SEASON COLS
# Much much faster, but results inconsistent with above
# Investigation in progress


# def create_months_column(ocean_data):
#     ocean_data["Month"] = 0
#     years_list = years()
#     months_list = months()
#     for year in years_list:
#         assign_months(year, months_list, ocean_data)
#         months_list += 12
#     return ocean_data


# def create_seasons_column(ocean_data):
#     ocean_data["Season"] = None
#     years_list = years()
#     seasons_list = ["winter", "spring", "summer", "autumn"]
#     for year in years_list:
#         assign_seasons(year, seasons_list, ocean_data)
#     return ocean_data

# def assign_months(year, months_list, ocean_data):
#     _year = ocean_data["Year"] == year
#     month_masks = get_month_masks(ocean_data)
#     for i in range(0, len(months_list)):
#         _month = month_masks[i]
#         _mask = _year & _month
#         ocean_data["Month"] = ocean_data["Month"].where(~_mask, other=months_list[i])


# def assign_seasons(year, seasons_list, ocean_data):
#     _year = ocean_data["Year"] == year
#     season_masks = get_season_masks(ocean_data)
#     for i in range(0, len(seasons_list)):
#         _season = season_masks[i]
#         _mask = _year & _season
#         ocean_data["Season"] = ocean_data["Season"].where(~_mask, other=seasons_list[i])


# def get_month_masks(ocean_data):
#     masks = [
#         ocean_data["Day"].between(1.0, 30.0, inclusive=True),
#         ocean_data["Day"].between(31.0, 59.0, inclusive=True),
#         ocean_data["Day"].between(60.0, 90.0, inclusive=True),
#         ocean_data["Day"].between(91.0, 120.0, inclusive=True),
#         ocean_data["Day"].between(121.0, 151.0, inclusive=True),
#         ocean_data["Day"].between(152.0, 181.0, inclusive=True),
#         ocean_data["Day"].between(182.0, 212.0, inclusive=True),
#         ocean_data["Day"].between(213.0, 243.0, inclusive=True),
#         ocean_data["Day"].between(244.0, 274.0, inclusive=True),
#         ocean_data["Day"].between(275.0, 305.0, inclusive=True),
#         ocean_data["Day"].between(306.0, 335.0, inclusive=True),
#         ocean_data["Day"].between(336.0, 360.0, inclusive=True),
#     ]
#     return masks


# def get_season_masks(ocean_data):
#     masks = [
#         ocean_data["Day"].between(336.0, 366.0, inclusive=True)
#         | ocean_data["Day"].between(1.0, 60.0, inclusive=True),
#         ocean_data["Day"].between(61.0, 152.0, inclusive=True),
#         ocean_data["Day"].between(153.0, 244.0, inclusive=True),
#         ocean_data["Day"].between(245.0, 335.0, inclusive=True),
#     ]
#     return masks
