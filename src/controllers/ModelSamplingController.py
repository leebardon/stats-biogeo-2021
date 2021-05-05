import numpy as np
import pandas as pd
import os
from pathlib import Path
from alive_progress import alive_bar, config_handler
import time

from ML_Biogeography_2021.models.sample_model import Sampling

base_path = Path(os.path.abspath(__file__)).parents[1] / "all_outputs"

ECOSYS_OCEAN = base_path / "model_whole_ocean_data" / "present" / "ecosys_ocean_p.pkl"
ECOSYS_OCEAN_FUTURE = (
    base_path / "model_whole_ocean_data" / "future" / "ecosys_ocean_f.pkl"
)
SALINITY_OCEAN = (
    base_path / "model_whole_ocean_data" / "present" / "salinity_ocean_p.pkl"
)
SALINITY_OCEAN_FUTURE = (
    base_path / "model_whole_ocean_data" / "future" / "salinity_ocean_f.pkl"
)
SST_OCEAN = base_path / "model_whole_ocean_data" / "present" / "sst_ocean_p.pkl"
SST_OCEAN_FUTURE = base_path / "model_whole_ocean_data" / "future" / "sst_ocean_f.pkl"
PAR_OCEAN = base_path / "model_whole_ocean_data" / "par_ocean.pkl"
SAMPLING_MATRIX = base_path / "sampling_matrices" / "sampling_matrix.npy"
RANDOM_SAMPLING_MATRIX = base_path / "sampling_matrices" / "random_sampling_matrix.npy"
WHOLE_OCEAN_SAVE = base_path / "model_whole_ocean_data"
SAVE_PATH = base_path / "sampled_model_data"


config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.02)

print("Obtaining sampling matrices and Darwin model ecosystem data...")
with alive_bar(3) as bar:
    I = np.load(SAMPLING_MATRIX)
    Ir = np.load(RANDOM_SAMPLING_MATRIX)
    bar()
    t
    I, Ir = Sampling.reshape_matrices(I, Ir)
    I_df, Ir_df = Sampling.return_dataframes(I, Ir)
    bar()
    t
    ecosys = pd.read_pickle(ECOSYS_OCEAN)
    ecosys_future = pd.read_pickle(ECOSYS_OCEAN_FUTURE)
    bar()
    t

print("Merging sampling matrices with ecosystem data...")
with alive_bar(1) as bar:  # for merging with sampling matrices
    merged_df = Sampling.merge_matrix_and_ecosys_data(I_df, ecosys)
    merged_random_df = Sampling.merge_matrix_and_ecosys_data(Ir_df, ecosys)
    bar()
    t

print("Removing data over land (pCO2 == 0)...")
with alive_bar(1) as bar:
    sampled_set = Sampling.remove_land(merged_df)
    randomly_sampled_set = Sampling.remove_land(merged_random_df)
    bar()
    t

print("Ensuring sampled subsets are equal size and saving...")
with alive_bar(2) as bar:
    sampled_set = Sampling.make_equal(sampled_set, randomly_sampled_set)
    bar()
    t
    sampled_set.to_pickle(f"{SAVE_PATH}/ecosys_sample_3586.pkl")
    randomly_sampled_set.to_pickle(f"{SAVE_PATH}/ecosys_random_sample_3586.pkl")
    bar()
    t
