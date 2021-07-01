import os
from time import sleep
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.models.sample_model import Sampling
from src.models import Save

ROOT = Path(os.path.abspath(__file__)).parents[2]

# Load
DARWIN = ROOT / "data" / "processed" / "model_ocean_data"
MATRICES = ROOT / "data" / "processed" / "sampling_matrices"
# Save
INTERIM = Save.check_dir_exists(f"{ROOT}/data/interim/sampled_ecosys")

config_handler.set_global(length=50, spinner="fish_bouncing")


print("Obtaining sampling matrices and Darwin model ecosystem data...")
with alive_bar(3) as bar:
    I, Ir, Ir2, Ir3 = Sampling.get_matrices(
        f"{MATRICES}",
        "ocean_sample_matrix",
        "random_sample_matrix",
        "random_matrix_2",
        "random_matrix_3",
    )
    bar()
    sleep(2)
    I, Ir, Ir2, Ir3 = Sampling.reshape_matrices(I, Ir, Ir2, Ir3)
    I_df, Ir_df, Ir2_df, Ir3_df = Sampling.return_dataframes(I, Ir, Ir2, Ir3)
    bar()
    sleep(2)
    ecosys, ecosys_future = Sampling.get_ecosys_data(
        f"{DARWIN}",
        "present/ecosys_ocean_p",
        "future/ecosys_ocean_f",
    )
    bar()
    sleep(2)

print("Merging sampling matrices with ecosystem data...")
with alive_bar(2) as bar:
    merged_df = Sampling.merge_matrix_and_ecosys_data(I_df, ecosys)
    merged_rand_df = Sampling.merge_matrix_and_ecosys_data(Ir_df, ecosys)
    merged_df_fut = Sampling.merge_matrix_and_ecosys_data(I_df, ecosys_future)
    merged_rand_df_fut = Sampling.merge_matrix_and_ecosys_data(Ir_df, ecosys_future)
    bar()
    sleep(2)
    merged_r2_df = Sampling.merge_matrix_and_ecosys_data(Ir2_df, ecosys)
    merged_r3_df = Sampling.merge_matrix_and_ecosys_data(Ir3_df, ecosys)
    merged_r2_df_fut = Sampling.merge_matrix_and_ecosys_data(Ir2_df, ecosys_future)
    merged_r3_df_fut = Sampling.merge_matrix_and_ecosys_data(Ir3_df, ecosys_future)

print("Removing data over land (pCO2 == 0)...")
with alive_bar(2) as bar:
    samp_oce = Sampling.remove_land(merged_df)
    rand_samp_oce = Sampling.remove_land(merged_rand_df)
    samp_oce_fut = Sampling.remove_land(merged_df_fut)
    rand_samp_oce_fut = Sampling.remove_land(merged_rand_df_fut)
    bar()
    sleep(2)
    r2_oce = Sampling.remove_land(merged_r2_df)
    r3_oce = Sampling.remove_land(merged_r3_df)
    r2_oce_fut = Sampling.remove_land(merged_r2_df_fut)
    r3_oce_fut = Sampling.remove_land(merged_r3_df_fut)
    bar()
    sleep(2)

print("Ensuring random sample is equal size to obvs sample and saving...")
with alive_bar(2) as bar:
    rand_samp_oce = Sampling.make_equal(samp_oce, rand_samp_oce)
    rand_samp_oce_fut = Sampling.make_equal(samp_oce_fut, rand_samp_oce_fut)
    bar()
    sleep(2)

    Save.save_to_pkl(
        f"{INTERIM}",
        **{
            "eco_samp_p.pkl": samp_oce,
            "rand_eco_samp_p.pkl": rand_samp_oce,
            "eco_samp_f.pkl": samp_oce_fut,
            "rand_eco_samp_f.pkl": rand_samp_oce_fut,
            "r2_samp.pkl": r2_oce,
            "r2_samp_f.pkl": r2_oce_fut,
            "r3_samp.pkl": r3_oce,
            "r3_samp_f.pkl": r3_oce_fut,
        },
    )
    bar()
    sleep(2)
