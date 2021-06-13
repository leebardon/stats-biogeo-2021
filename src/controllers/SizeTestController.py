import time
import os
import numpy as np
import pandas as pd
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.models import Save
from src.models.build_training_sets import TrainingSetBuilder as TSB
from src.models.sample_size_testing import SizeTestMatrices, SizeTestSampling

ROOT = Path(os.path.abspath(__file__)).parents[2]
INTERIM = ROOT / "data" / "interim"
OCEAN = ROOT / "data" / "processed" / "model_ocean_data"

config_handler.set_global(length=50, spinner="fish_bouncing")
t = time.sleep(2)
TEST_MATRIX_SEEDS = [np.arange(19)]


print("Generating 18 random sampling matrices from (N=100 .. N=18,000)...")
with alive_bar(1) as bar:

    matrices, num_cells = SizeTestMatrices.random_test_matrices(TEST_MATRIX_SEEDS)
    Save.size_test_matrices(INTERIM, matrices, num_cells)
    bar()
    t


print("Obtaining Darwin ecosystem and physical data...")
with alive_bar(1) as bar:
    ecosys = pd.read_pickle(f"{OCEAN}/present/ecosys_ocean_p.pkl")
    salinity_oce, sst_oce, par_oce = TSB.get_data(
        f"{OCEAN}/present",
        *[
            "sss_ocean_p.pkl",
            "sst_ocean_p.pkl",
            "par_ocean.pkl",
        ],
    )
    bar()
    t

print("Merging randomly-sampled test matrices with ecosystem data...")
with alive_bar(1) as bar:
    reshaped = SizeTestSampling.reshape_test_matrices(matrices)
    dataframes = SizeTestSampling.return_test_dataframes(reshaped)
    merged = SizeTestSampling.merge_test_matrices_and_ecosys_data(dataframes, ecosys)
    sampled_ecosys_dfs = SizeTestSampling.check_land_removed(merged)

    Save.size_test_sampled_ecosys(INTERIM, sampled_ecosys_dfs)
    bar()
    t




