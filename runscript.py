import os, sys

sys.path.insert(0, os.path.abspath("."))

from pathlib import Path
import os, sys
from subprocess import run

base_path = Path(os.path.abspath(__file__)).parents[0] / "src" / "controllers"

# process_ocean_data = base_path / "OceanMeasurementsController.py"
# process_model_data = base_path / "ModelDataController.py"
# sample_model_data = base_path / "ModelSamplingController.py"
# build_training_sets = base_path / "TrainingSetController.py"
# train_gams = base_path / "GamsController.py"
analyse_results = base_path / "AnalysisController.py"
# final_figs = base_path / "FinalFigsController.py"


# run(["python", f"{process_ocean_data}"])
# run(["python", f"{process_model_data}"])
# run(["python", f"{sample_model_data}"])
# un(["python", f"{build_training_sets}"])
# run(["python", f"{train_gams}"])
run(["python", f"{analyse_results}"])
# run(["python", f"{final_figs}"])


# put cli interface stuff in here, i.e. an options menu
# so they don't have to do the whole process every time
