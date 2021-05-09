import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import numpy as np
import pandas as pd
import xarray as xr
import time
from alive_progress import alive_bar, config_handler
from pathlib import Path
from src.models import Save
from src.models.extract_model_data import (
    GetEcosysData,
    GetPhysicalData,
    CombineDatasets,
)

base_path = Path(os.path.abspath(__file__)).parents[2]
RAW = base_path / "data" / "raw"
INTERIM = base_path / "data" / "interim" / "darwin_interim_data"
DARWIN = base_path / "data" / "processed"
DEPTH = 0


config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.02)

# note
# Here we start with surface data that has already been extracted
# from remote MIT servers that store raw Darwin outputs.
# The relevant code is in GetEcosysData.py and GetPhysicalData.py
print("Extracting surface data from Darwin model & removing land (pCO2 == 0)...")
with alive_bar(2) as bar:
    ecosys_interim_df = f"{INTERIM}/present/ecosys_interim_p.pkl"
    # ecosys_interim_df = GetEcosysData.get_ecosys_surface_data(
    #     f"{RAW}/ecosystem/present"
    # )
    # Save.save_as_pkl(ecosys_interim_df, f"{INTERIM}/present", "ecosys_interim_p.pkl")
    bar()
    t
    ecosys_interim_df_fut = f"{INTERIM}/future/ecosys_interim_f.pkl"
    # ecosys_interim_df_fut = GetEcosysData.get_ecosys_surface_data(
    #     f"{RAW}/ecosystem/future"
    # )
    # Save.save_as_pkl(ecosys_interim_df_fut, f"{INTERIM}/future", "ecosys_interim_f.pkl")
    bar()
    t

print("Mapping lat and lon degrees to grid coords and saving...")
with alive_bar(2) as bar:
    ecosys_df = GetEcosysData.add_grid_coords(ecosys_interim_df)
    ecosys_future_df = GetEcosysData.add_grid_coords(ecosys_interim_df_fut)
    bar()
    t
    Save.save_to_pkl(
        ecosys_df, f"{DARWIN}/model_ocean_data/present", "ecosys_ocean_p.pkl"
    )
    Save.save_to_pkl(
        ecosys_df, f"{DARWIN}/model_ocean_data/future", "ecosys_ocean_f.pkl"
    )
    bar()
    t


print("Extracting surface physical data from Darwin model, removing land (x == 0)...")
with alive_bar(3) as bar:
    # salinity_df, salinity_matrix = GetPhysicalData.get_phys_surface_data(
    #     f"{RAW}/physical/SSS/present", "SSS"
    # )
    Save.save_to_pkl(
        salinity_df, f"{DARWIN}/model_ocean_data/present", "sss_ocean_p.pkl"
    )
    Save.save_matrix(
        salinity_matrix, f"{DARWIN}/model_ocean_data/present", "sss_matrix_p.npy"
    )
    # salinity_f_df, salinity_f_matrix = GetPhysicalData.get_phys_surface_data(
    #     f"{RAW}/physical/SSS/future", "SSS"
    # )
    Save.save_to_pkl(
        salinity_f_df, f"{DARWIN}/model_ocean_data/future", "sss_ocean_f.pkl"
    )
    Save.save_matrix(
        salinity_f_matrix, f"{DARWIN}/model_ocean_data/future", "sss_matrix_f.npy"
    )
    bar()
    t
    # sst_df, sst_matrix = GetPhysicalData.get_phys_surface_data(
    #     f"{RAW}/physical/SST/present", "SST"
    # )
    Save.save_to_pkl(sst_df, f"{DARWIN}/model_ocean_data/present", "sst_ocean.pkl")
    Save.save_matrix(sst_matrix, f"{DARWIN}/model_ocean_data/present", "sst_matrix.npy")
    # sst_f_df, sst_f_matrix = GetPhysicalData.get_phys_surface_data(
    #     f"{RAW}/physical/SST/future", "SST"
    # )
    Save.save_to_pkl(sst_f_df, f"{DARWIN}/model_ocean_data/future", "sst_ocean_f.pkl")
    Save.save_matrix(
        sst_f_matrix, f"{DARWIN}/model_ocean_data/future", "sst_matrix_f.npy"
    )
    bar()
    t
    par, par_matrix = GetPhysicalData.get_par_data(
        f"{RAW}/physical/PAR", "PAR", 23, 265, salinity
    )
    Save.save_to_pkl(par_df, f"{DARWIN}/model_ocean_data", "par_ocean.pkl")
    Save.save_matrix(par_matrix, f"{DARWIN}/model_ocean_data", "par_matrix.npy")
    bar()
    t
