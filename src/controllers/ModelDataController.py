import os
import pandas as pd
from subprocess import run
from time import sleep
from alive_progress import alive_bar, config_handler
from pathlib import Path
from src.models import Save
from src.models.extract_model_data import GetEcosysData, GetPhysicalData

ROOT = Path(os.path.abspath(__file__)).parents[2]
DEPTH = 0

# Load
RAW = ROOT / "data" / "raw"
INTERIM = ROOT / "data" / "interim" / "whole_ecosys"
# Save
PROCESSED = Save.check_dir_exists(f"{ROOT}/data/processed")

config_handler.set_global(length=50, spinner="fish_bouncing")


# NOTE:
# If there is no raw Darwin .nc data in correct folder, system will revert
# to using pre-extracted and processed surface data in interim/whole_ecosys dir

print("Extracting surface data from Darwin model & removing land (pCO2 == 0)...")
with alive_bar(2) as bar:
    try:
        if os.listdir(f"{RAW}/ecosystem"):
            ecosys_interim_df = GetEcosysData.get_ecosys_surface_data(
                f"{RAW}/ecosystem/present"
            )
            bar()
            sleep(2)
            ecosys_interim_df_fut = GetEcosysData.get_ecosys_surface_data(
                f"{RAW}/ecosystem/future"
            )
            Save.save_to_pkl(
                f"{INTERIM}",
                **{
                    "ecosys_interim_p.pkl": ecosys_interim_df,
                    "ecosys_interim_f.pkl": ecosys_interim_df_fut,
                },
            )
            bar()
            sleep(2)

    except:
        print(
            f" \n ERROR: Please add raw Darwin ecosystem data into: {RAW}/ecosystem...!"
        )
        run(["python", f"{ROOT}/runscript.py"])

    finally:
        ecosys_interim_df = pd.read_pickle(f"{INTERIM}/ecosys_interim_p.pkl")
        ecosys_interim_df_fut = pd.read_pickle(f"{INTERIM}/ecosys_interim_f.pkl")


print("Mapping lat and lon degrees to grid coords...")
with alive_bar(2) as bar:
    try:
        ecosys = GetEcosysData.add_grid_coords(ecosys_interim_df)
        ecosys_f = GetEcosysData.add_grid_coords(ecosys_interim_df_fut)
        bar()
        sleep(2)
        Save.save_to_pkl(
            Save.check_dir_exists(f"{PROCESSED}/model_ocean_data/present"),
            **{"ecosys_ocean_p.pkl": ecosys},
        )
        Save.save_to_pkl(
            Save.check_dir_exists(f"{PROCESSED}/model_ocean_data/future"),
            **{"ecosys_ocean_f.pkl": ecosys_f},
        )
        bar()
        sleep(2)

    except:
        print(f" \n ERROR: Problem mapping lat and lon degrees to grid coords... ")
        run(["python", f"{ROOT}/runscript.py"])


print("Extracting surface physical data from Darwin model, removing land (x == 0)...")
with alive_bar(4) as bar:
    try:
        if os.listdir(f"{RAW}/physical"):
            salinity_df, salinity_matrix = GetPhysicalData.get_phys_surface_data(
                f"{RAW}/physical/SSS/present", "SSS"
            )
            salinity_f_df, salinity_f_matrix = GetPhysicalData.get_phys_surface_data(
                f"{RAW}/physical/SSS/future", "SSS"
            )
            bar()
            sleep(2)
            sst_df, sst_matrix = GetPhysicalData.get_phys_surface_data(
                f"{RAW}/physical/SST/present", "SST"
            )
            sst_f_df, sst_f_matrix = GetPhysicalData.get_phys_surface_data(
                f"{RAW}/physical/SST/future", "SST"
            )
            bar()
            sleep(2)
            par_df, par_matrix = GetPhysicalData.get_par_data(
                f"{RAW}/physical/PAR", "PAR", 23, 265, salinity_df
            )
            bar()
            sleep(2)
            Save.save_to_pkl(
                f"{PROCESSED}/model_ocean_data/present",
                **{
                    "sss_ocean_p.pkl": salinity_df,
                    "sst_ocean_p.pkl": sst_df,
                    "par_ocean.pkl": par_df,
                },
            )
            Save.save_to_pkl(
                f"{PROCESSED}/model_ocean_data/future",
                **{
                    "sss_ocean_f.pkl": salinity_f_df,
                    "sst_ocean_f.pkl": sst_f_df,
                    "par_ocean.pkl": par_df,
                },
            )
            Save.save_matrix(
                f"{PROCESSED}/model_ocean_data/present",
                **{
                    "sss_matrix_p.npy": salinity_matrix,
                    "sst_matrix_p.npy": sst_matrix,
                    "par_matrix.npy": par_matrix,
                },
            )
            Save.save_matrix(
                f"{PROCESSED}/model_ocean_data/future",
                **{
                    "sss_matrix_f.npy": salinity_f_matrix,
                    "sst_matrix_f.npy": sst_f_matrix,
                    "par_matrix.npy": par_matrix,
                },
            )
            bar()
            sleep(2)

    except:
        print(f" \n ERROR: Please add SST, SSS, and PAR data into: {RAW}/physical...!")
        run(["python", f"{ROOT}/runscript.py"])

    print(f"\n --Completed, returning to main menu-- ")
    run(["python", f"{ROOT}/runscript.py"])
