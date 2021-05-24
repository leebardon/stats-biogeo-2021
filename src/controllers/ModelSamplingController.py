import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "..", "..", "..")))

import numpy as np
import pandas as pd
import time
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.models.sample_model import Sampling
from src.models import Save

base_path = Path(os.path.abspath(__file__)).parents[2]

DARWIN = base_path / "data" / "processed" / "model_ocean_data"
MATRICES = base_path / "data" / "processed" / "sampling_matrices"
INTERIM = base_path / "data" / "interim" / "sampled_ecosys"

config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(2)

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
    merged_rand_df = Sampling.merge_matrix_and_ecosys_data(Ir_df, ecosys)
    merged_df_fut = Sampling.merge_matrix_and_ecosys_data(I_df, ecosys_future)
    merged_rand_df_fut = Sampling.merge_matrix_and_ecosys_data(Ir_df, ecosys_future)
    bar()
    t

print("Removing data over land (pCO2 == 0)...")
with alive_bar(1) as bar:
    samp_oce = Sampling.remove_land(merged_df)
    rand_samp_oce = Sampling.remove_land(merged_rand_df)
    samp_oce_fut = Sampling.remove_land(merged_df_fut)
    rand_samp_oce_fut = Sampling.remove_land(merged_rand_df_fut)
    bar()
    t

print("Ensuring random sample is equal size to obvs sample and saving...")
with alive_bar(2) as bar:
    rand_samp_oce = Sampling.make_equal(samp_oce, rand_samp_oce)
    rand_samp_oce_fut = Sampling.make_equal(samp_oce_fut, rand_samp_oce_fut)
    bar()
    t

    Save.save_to_pkl(
        f"{INTERIM}",
        **{
            "eco_samp_p.pkl": samp_oce,
            "rand_eco_samp_p.pkl": rand_samp_oce,
            "eco_samp_f.pkl": samp_oce_fut,
            "rand_eco_samp_f.pkl": rand_samp_oce_fut,
        },
    )
    bar()
    t
