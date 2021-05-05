### Change to allow saving in different forms - df, matrix, matlab, csv
### Generalise to extract at user-given depth

import numpy as np
import pandas as pd
import xarray as xr
import os
from alive_progress import alive_bar, config_handler
import time
from pathlib import Path

from ML_Biogeography_2021.models.extract_model_data import (
    GetEcosysData,
    GetPhysicalData,
    CombineDatasets,
)

base_path = Path(os.path.abspath(__file__)).parents[1]

# Target folders for .nc Files (Ecosystem), .data files (physical) and saving results
SAVE_PATH = base_path / "all_outputs" / "model_whole_ocean_data"
ECOSYS_PATH = base_path / "test_data" / "test_ecosys_data"
SALINITY_PATH = (
    base_path / "all_outputs" / "model_whole_ocean_data" / "present" / "sss_ocean_p.pkl"
)
SST_PATH = base_path / "test_data" / "test_SST_data"
PAR_PATH = (
    base_path / "test_data" / "test_PAR_data" / "igsm_oasim_etotal_below_einm2d.bin"
)
DEPTH = 0


config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.02)

print("Extracting surface data from Darwin model, removing land (pCO2 == 0)...")
with alive_bar(2) as bar:
    ecosys_df = GetEcosysData.get_ecosys_surface_data(ECOSYS_PATH)
    bar()
    t
    ecosys_df_future = GetEcosysData.get_ecosys_surface_data(ECOSYS_FUTURE_PATH)
    bar()
    t

print("Mapping lat and lon degrees to grid coords...")
with alive_bar(2) as bar:
    ecosys_df = GetEcosysData.add_grid_coords(ecosys_df)
    ecosys_future_df = GetEcosysData.add_grid_coords(ecosys_future_df)
    bar()
    t
    # ecosys_df.to_pickle(f"{SAVE_PATH}/test_ecosys_present.pkl")
    ecosys_df.to_pickle(f"{SAVE_PATH}/present/ecosys_ocean_p.pkl")
    ecosys_df_future.to_pickle(f"{SAVE_PATH}/future/ecosys_ocean_f.pkl")
    bar()
    t


print("Extracting surface physical data from Darwin model, removing land (x == 0)...")
with alive_bar(3) as bar:
    salinity, salinity_matrix = GetPhysicalData.get_phys_surface_data(
        SALINITY_PATH, "SSS"
    )
    salinity.to_pickle(f"{SAVE_PATH}/raw_extracted_data/present/sss_ocean_p.pkl")
    np.save(
        f"{SAVE_PATH}/raw_extracted_data/present/sss_matrix_p",
        salinity_matrix,
        allow_pickle=True,
    )

    salinity_f, salinity_matrix_f = GetPhysicalData.get_phys_surface_data(
        SALINITY_FUTURE_PATH, "SSS"
    )
    salinity_f.to_pickle(f"{SAVE_PATH}/raw_extracted_data/future/sss_ocean_f.pkl")
    np.save(
        f"{SAVE_PATH}/raw_extracted_data/future/sss_matrix_f",
        salinity_matrix,
        allow_pickle=True,
    )
    bar()
    t
    sst, sst_matrix = GetPhysicalData.get_phys_surface_data(SST_PATH, "SST")
    sst.to_pickle(f"{SAVE_PATH}/raw_extracted_data/present/sst_ocean_p.pkl")
    np.save(
        f"{SAVE_PATH}/raw_extracted_data/present/sst_matrix_p",
        sst_matrix,
        allow_pickle=True,
    )

    sst_f, sst_matrix_f = GetPhysicalData.get_phys_surface_data(SST_FUTURE_PATH, "SST")
    sst_f.to_pickle(f"{SAVE_PATH}/raw_extracted_data/future/sst_ocean_f.pkl")
    # np.save(f"{SAVE_PATH}/raw_extracted_data/future/sst_matrix_f", sst_matrix_f, allow_pickle=True)
    bar()
    t
    salinity = pd.read_pickle(f"{SALINITY_PATH}")
    par, par_matrix = GetPhysicalData.get_par_data(PAR_PATH, "PAR", 23, 265, salinity)
    par.to_pickle(f"{SAVE_PATH}/par_ocean.pkl")
    # np.save(f"{SAVE_PATH}/par_matrix", allow_pickle=True)
    bar()
    t
