import xarray as xr
import os
import sys
from time import sleep
from pathlib import Path
from alive_progress import alive_bar, config_handler
from src.views import MatrixPlots
from src.models import Save, Utils
from src.models.sample_measurements import (
    CleanData,
    AddColumns,
    CreateSamplingMatrix,
)

ROOT = Path(os.path.abspath(__file__)).parents[2]
SEED, SEED2, SEED3 = 2021_1, 2021_2, 2021_3

# Load
OCEAN_OBVS = ROOT / "data" / "raw" / "ocean_observations.netcdf"
GRID_CELL = ROOT / "data" / "raw" / "grid_igsm.nc"
# Save
SAVEPATH = Save.check_dir_exists(f"{ROOT}/data/processed")
PLOTPATH = Save.check_dir_exists(f"{ROOT}/results/all_plots/sample_distributions")


log = Utils.setup_logger("syslog")
scilog = Utils.setup_logger("scilog_ocean_meas")
config_handler.set_global(length=50, spinner="fish_bouncing")


print("Obtaining ocean measurements dataset...")
with alive_bar(1) as bar:
    try:
        ocean_measurements_data = xr.open_dataset(OCEAN_OBVS)
        raw_measurements_df = ocean_measurements_data.to_dataframe()
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem obtaining measurements .netcdf dataset ...")
        sys.exit(1)


print("Decoding bytes objects and coercing to floats...")
with alive_bar(1) as bar:
    try:
        ocean_measurements_df = CleanData.decode_all_columns(raw_measurements_df)
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem Decoding bytes objects and coercing to floats...")
        sys.exit(1)


print("Drop erroneous data (Year > 2.008e+03 ; Day > 9.96e+30)...")
with alive_bar(1) as bar:
    try:
        ocean_measurements_df = CleanData.drop_erroneous(ocean_measurements_df)
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem dropping erroneous data......")
        sys.exit(1)


print("Adding 'Months' columns and saving processed dataset...")
with alive_bar(2) as bar:
    try:
        processed_ocean_df = AddColumns.create_months_column(ocean_measurements_df)
        # processed_ocean_df = AddColumns.create_seasons_column(measurements_df_plus_months)
        bar()
        sleep(2)

        Save.save_to_pkl(
            f"{SAVEPATH}/ocean_measurement_data",
            **{"cleaned_meas_data.pkl": processed_ocean_df},
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem adding months column......")
        sys.exit(1)


print("Obtaining vectors of ocean measurements' lon, lat & time (mon 1 -> 264)...")
with alive_bar(1) as bar:
    try:
        X, Y, T = CreateSamplingMatrix.column_coordinates(processed_ocean_df)
        raw_matrix = CreateSamplingMatrix.raw_matrix(X, Y, T)
        ocean_measurements_matrix = CreateSamplingMatrix.clean_matrix(raw_matrix)
        X, Y, T = CreateSamplingMatrix.matrix_coordinates(
            ocean_measurements_matrix, type=1
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem obtaining vectors of ocean measurements......")
        sys.exit(1)


print("Obtaining vectors of Darwin cell centre's lon, lat & time (mon 1 -> 264)...")
with alive_bar(1) as bar:
    try:
        grid_cell_centres = xr.open_dataset(GRID_CELL)
        x, y, t = CreateSamplingMatrix.matrix_coordinates(grid_cell_centres, type=2)
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem obtaining vectors of Darwin cell centres......")
        sys.exit(1)


print("Generating and saving sampling matrices...")
with alive_bar(3) as bar:
    try:
        I_zeros = CreateSamplingMatrix.matrix_of_zeros()
        I = CreateSamplingMatrix.sampling_matrix(I_zeros, X, Y, T, x, y)
        bar()
        t
        Ir = CreateSamplingMatrix.random_matrix(SEED, 10000)
        Ir2 = CreateSamplingMatrix.random_matrix(SEED2, 20000)
        Ir3 = CreateSamplingMatrix.random_matrix(SEED3, 40000)
        bar()
        t
        Save.save_matrix(
            f"{SAVEPATH}/sampling_matrices",
            **{
                "ocean_sample_matrix.npy": I,
                "random_sample_matrix.npy": Ir,
                "random_matrix_2.npy": Ir2,
                "random_matrix_3.npy": Ir3,
            },
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem generating sampling matrices......")
        sys.exit(1)


print("Generating and saving sample distribution plots...")
with alive_bar(4) as bar:
    try:
        MatrixPlots.matrix_scatter_plot(
            I,
            PLOTPATH,
            "ocean_measurements_scatterplot",
            dtype="Observational",
        )
        bar()
        sleep(2)

        MatrixPlots.matrix_histogram(
            I,
            PLOTPATH,
            "ocean_measurements_histogram",
            dtype="Observational",
        )
        bar()
        sleep(2)

        MatrixPlots.matrix_scatter_plot(
            Ir, PLOTPATH, "random_sample_scatterplot", dtype="Random"
        )
        bar()
        sleep(2)

        MatrixPlots.matrix_histogram(
            Ir, PLOTPATH, "random_sample_histogram", dtype="Random"
        )
        bar()
        sleep(2)

    except:
        print(" \n ERROR: Problem generating plots......")
        sys.exit(1)

    sys.exit(1)
