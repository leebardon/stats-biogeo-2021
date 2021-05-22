import numpy as np
import pandas as pd


def create_months_column(ocean_data):
    ocean_data["Month"] = 0
    years_list = years()
    months_list = months()
    for year in years_list:
        assign_months(year, months_list, ocean_data)
        months_list = months_list + 12
    return ocean_data


def create_seasons_column(ocean_data):
    ocean_data["Season"] = None
    years_list = years()
    seasons_list = ["winter", "spring", "summer", "autumn"]
    for year in years_list:
        assign_seasons(year, seasons_list, ocean_data)
    return ocean_data


def years():
    return [i for i in np.arange(1987.0, 2009.0, 1)]


def months():
    return pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])


def assign_months(year, months_list, ocean_data):
    _year = ocean_data["Year"] == year
    month_masks = get_month_masks()
    for i in range(0, len(months_list)):
        _month = month_masks[i]
        _mask = _year & _month
        ocean_data["Month"] = ocean_data["Month"].where(~_mask, other=months_list[i])


def assign_seasons(year, seasons_list, ocean_data):
    _year = ocean_data["Year"] == year
    season_masks = get_season_masks()
    for i in range(0, len(seasons_list)):
        _season = season_masks[i]
        _mask = _year & _season
        ocean_data["Season"] = ocean_data["Season"].where(~_mask, other=seasons_list[i])


def get_month_masks():
    masks = [
        ocean_data["Day"].between(1.0, 32.0, inclusive=True),
        ocean_data["Day"].between(32.0, 60.0, inclusive=True),
        ocean_data["Day"].between(61.0, 91.0, inclusive=True),
        ocean_data["Day"].between(92.0, 121.0, inclusive=True),
        ocean_data["Day"].between(122.0, 152.0, inclusive=True),
        ocean_data["Day"].between(153.0, 182.0, inclusive=True),
        ocean_data["Day"].between(183.0, 213.0, inclusive=True),
        ocean_data["Day"].between(214.0, 244.0, inclusive=True),
        ocean_data["Day"].between(245.0, 274.0, inclusive=True),
        ocean_data["Day"].between(275.0, 305.0, inclusive=True),
        ocean_data["Day"].between(306.0, 335.0, inclusive=True),
        ocean_data["Day"].between(336.0, 366.0, inclusive=True),
    ]
    return masks


def get_season_masks():
    masks = [
        ocean_data["Day"].between(336.0, 366.0, inclusive=True)
        | ocean_data["Day"].between(1.0, 60.0, inclusive=True),
        ocean_data["Day"].between(61.0, 152.0, inclusive=True),
        ocean_data["Day"].between(153.0, 244.0, inclusive=True),
        ocean_data["Day"].between(245.0, 335.0, inclusive=True),
    ]
    return masks
