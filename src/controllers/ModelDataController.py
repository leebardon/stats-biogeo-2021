import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import numpy as np
import pandas as pd
import xarray as xr
import time
from alive_progress import alive_bar, config_handler
from pathlib import Path

from src.models.extract_model_data import (
    GetEcosysData,
    GetPhysicalData,
    CombineDatasets,
)

base_path = Path(os.path.abspath(__file__)).parents[2]
SAVE_PATH = base_path / "data" / "processed"
DARWIN = base_path / "data" / "processed" / "model_whole_ocean_data"
DEPTH = 0


config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.02)

print("Extracting surface data from Darwin model, removing land (pCO2 == 0)...")
with alive_bar(2) as bar:
    ecosys_df = GetEcosysData.get_ecosys_surface_data(
        f"{DARWIN}/present/ecosys_ocean_p.pkl"
    )
    bar
    t
    ecosys_df_future = GetEcosysData.get_ecosys_surface_data(
        f"{DARWIN}/future/ecosys_ocean_f.pkl"
    )
    bar
    t

print("Mapping lat and lon degrees to grid coords...")
with alive_bar(2) as bar:
    ecosys_df = GetEcosysData.add_grid_coords(ecosys_df)
    ecosys_future_df = GetEcosysData.add_grid_coords(ecosys_future_df)
    bar
    t
    # ecosys_df.to_pickle(f"{SAVE_PATH}/test_ecosys_present.pkl")
    ecosys_df.to_pickle(
        f"{SAVE_PATH}/model_whole_ocean_data/present/ecosys_ocean_p.pkl"
    )
    ecosys_df_future.to_pickle(
        f"{SAVE_PATH}/model_whole_ocean_data/future/ecosys_ocean_f.pkl"
    )
    bar
    t


print("Extracting surface physical data from Darwin model, removing land (x == 0)...")
with alive_bar(3) as bar:
    salinity, salinity_matrix = GetPhysicalData.get_phys_surface_data(
        f"{DARWIN}/present/sss_ocean_p.pkl", "SSS"
    )
    salinity.to_pickle(f"{SAVE_PATH}/raw_extracted_data/present/sss_ocean_p.pkl")
    np.save(
        f"{SAVE_PATH}/raw_extracted_data/present/sss_matrix_p",
        salinity_matrix,
        allow_pickle=True,
    )

    salinity_f, salinity_matrix_f = GetPhysicalData.get_phys_surface_data(
        f"{DARWIN}/future/sss_ocean_f.pkl", "SSS"
    )
    salinity_f.to_pickle(f"{SAVE_PATH}/raw_extracted_data/future/sss_ocean_f.pkl")
    np.save(
        f"{SAVE_PATH}/raw_extracted_data/future/sss_matrix_f",
        salinity_matrix,
        allow_pickle=True,
    )
    bar()
    t
    sst, sst_matrix = GetPhysicalData.get_phys_surface_data(
        f"{DARWIN}/present/sst_ocean_p.pkl", "SST"
    )
    sst.to_pickle(f"{SAVE_PATH}/raw_extracted_data/present/sst_ocean_p.pkl")
    np.save(
        f"{SAVE_PATH}/raw_extracted_data/present/sst_matrix_p",
        sst_matrix,
        allow_pickle=True,
    )

    sst_f, sst_matrix_f = GetPhysicalData.get_phys_surface_data(
        f"{DARWIN}/future/sss_ocean_f.pkl", "SST"
    )
    sst_f.to_pickle(f"{SAVE_PATH}/raw_extracted_data/future/sst_ocean_f.pkl")
    # np.save(f"{SAVE_PATH}/raw_extracted_data/future/sst_matrix_f", sst_matrix_f, allow_pickle=True)
    bar()
    t
    salinity = pd.read_pickle(f"{DARWIN}/present/sss_ocean_p.pkl")
    par, par_matrix = GetPhysicalData.get_par_data(
        f"{DARWIN}/par_ocean.pkl", "PAR", 23, 265, salinity
    )
    par.to_pickle(f"{SAVE_PATH}/par_ocean.pkl")
    # np.save(f"{SAVE_PATH}/par_matrix", allow_pickle=True)
    bar()
    t
