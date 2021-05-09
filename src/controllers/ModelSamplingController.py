import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import numpy as np
import pandas as pd
import time
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.models.sample_model import Sampling

base_path = Path(os.path.abspath(__file__)).parents[2]

DARWIN = base_path / "data" / "processed" / "model_whole_ocean_data"
MATRICES = base_path / "data" / "processed" / "sampling_matrices"
SAMPLES = base_path / "data" / "processed" / "model_sampled_data"

config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(0.02)

print("Obtaining sampling matrices and Darwin model ecosystem data...")
with alive_bar(3) as bar:
    I = np.load(f"{MATRICES}/ocean_sample_matrix.npy")
    Ir = np.load(f"{MATRICES}/random_sample_matrix.npy")
    bar()
    t
    I, Ir = Sampling.reshape_matrices(I, Ir)
    I_df, Ir_df = Sampling.return_dataframes(I, Ir)
    bar()
    t
    ecosys = pd.read_pickle(f"{DARWIN}/present/ecosys_ocean_p.pkl")
    ecosys_future = pd.read_pickle(f"{DARWIN}/future/ecosys_ocean_f.pkl")
    bar()
    t

print("Merging sampling matrices with ecosystem data...")
with alive_bar(1) as bar:
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
    sampled_set.to_pickle(f"{SAMPLES}/ecosys_sample_3586.pkl")
    randomly_sampled_set.to_pickle(f"{SAMPLES}/random_ecosys_sample_3586.pkl")
    bar()
    t
