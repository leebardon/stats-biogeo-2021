import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import numpy as np
import pandas as pd
import xarray as xrS
import time
from alive_progress import alive_bar, config_handler
from pathlib import Path
from src.models import Save
from src.models.extract_model_data import GetEcosysData, GetPhysicalData

# CombineDatasets - apparently this was a module I was gonna create :/ ??
# CREATE METHOD TO PRODUCE OUTPUT FILES of shape, min(X) max(X) etc

base_path = Path(os.path.abspath(__file__)).parents[2]
RAW = base_path / "data" / "raw"
INTERIM = base_path / "data" / "interim" / "whole_ecosys"
PROCESSED = base_path / "data" / "processed"
DEPTH = 0


config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(1)

# Note:
# Here we start with surface data that has already been extracted
# from remote MIT servers that store raw Darwin outputs.
# The relevant code is in GetEcosysData.py and GetPhysicalData.py
print("Extracting surface data from Darwin model & removing land (pCO2 == 0)...")
with alive_bar(3) as bar:
    # ecosys_interim_df = GetEcosysData.get_ecosys_surface_data(
    #     f"{RAW}/ecosystem/present"
    # )
    # bar()
    # t
    # ecosys_interim_df_fut = GetEcosysData.get_ecosys_surface_data(
    #     f"{RAW}/ecosystem/future"
    # )
    # bar()
    # t
    # Save.save_to_pkl(
    #     f"{INTERIM}",
    #     **{
    #         "ecosys_interim_p.pkl": ecosys_interim_df,
    #         "ecosys_interim_f.pkl": ecosys_interim_df_fut,
    #     },
    # )
    # bar()
    # t

    ecosys_interim = pd.read_pickle(f"{INTERIM}/ecosys_interim_p.pkl")
    ecosys_interim_f = pd.read_pickle(f"{INTERIM}/ecosys_interim_f.pkl")

print("Mapping lat and lon degrees to grid coords...")
with alive_bar(2) as bar:
    ecosys = GetEcosysData.add_grid_coords(ecosys_interim)
    ecosys_f = GetEcosysData.add_grid_coords(ecosys_interim_f)
    bar()
    t

    # print("Adding 'Seasons' column and saving...")
    # with alive_bar(2) as bar:
    # NOT WORKING
    # ecosys = GetEcosysData.add_seasons_col(ecosys)
    # ecosys_f = GetEcosysData.add_seasons_col(ecosys_f)
    # bar()
    # t

    Save.save_to_pkl(
        f"{PROCESSED}/model_ocean_data/present", **{"new_ecosys_ocean_p.pkl": ecosys}
    )
    Save.save_to_pkl(
        f"{PROCESSED}/model_ocean_data/future",
        **{"new_ecosys_ocean_f.pkl": ecosys_f},
    )
    bar()
    t

# print("Extracting surface physical data from Darwin model, removing land (x == 0)...")
# with alive_bar(4) as bar:
#     salinity_df, salinity_matrix = GetPhysicalData.get_phys_surface_data(
#         f"{RAW}/physical/SSS/present", "SSS"
#     )
#     salinity_f_df, salinity_f_matrix = GetPhysicalData.get_phys_surface_data(
#         f"{RAW}/physical/SSS/future", "SSS"
#     )
#     bar()
#     t
#     sst_df, sst_matrix = GetPhysicalData.get_phys_surface_data(
#         f"{RAW}/physical/SST/present", "SST"
#     )
#     sst_f_df, sst_f_matrix = GetPhysicalData.get_phys_surface_data(
#         f"{RAW}/physical/SST/future", "SST"
#     )
#     bar()
#     t
#     par_df, par_matrix = GetPhysicalData.get_par_data(
#         f"{RAW}/physical/PAR", "PAR", 23, 265, salinity_df
#     )
#     bar()
#     t
#     Save.save_to_pkl(
#         f"{PROCESSED}/model_ocean_data/present",
#         **{
#             "sss_ocean_p.pkl": salinity_df,
#             "sst_ocean_p.pkl": sst_df,
#             "par_ocean.pkl": par_df,
#         },
#     )
#     Save.save_to_pkl(
#         f"{PROCESSED}/model_ocean_data/future",
#         **{
#             "sss_ocean_f.pkl": salinity_f_df,
#             "sst_ocean_f.pkl": sst_f_df,
#             "par_ocean.pkl": par_df,
#         },
#     )
#     Save.save_matrix(
#         f"{PROCESSED}/model_ocean_data/present",
#         **{
#             "sss_matrix_p.npy": salinity_matrix,
#             "sst_matrix_p.npy": sst_matrix,
#             "par_matrix.npy": par_matrix,
#         },
#     )
#     Save.save_matrix(
#         f"{PROCESSED}/model_ocean_data/future",
#         **{
#             "sss_matrix_f.npy": salinity_f_matrix,
#             "sst_matrix_f.npy": sst_f_matrix,
#             "par_matrix.npy": par_matrix,
#         },
#     )
#     bar()
#     t
