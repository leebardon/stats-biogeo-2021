import os
import pytest
from pathlib import Path
import pandas as pd

BASE = Path(os.path.abspath(__file__)).parents[1]
DATA = BASE / "data" / "processed"

from src.models.gams import TrainGams

@pytest.fixture
def plankton():
    return pd.read_pickle(f"{DATA}/sampled_plankton/plankton.pkl")

@pytest.fixture
def predictors():
    return pd.read_pickle(f"{DATA}/sampled_predictors/predictors.pkl")

@pytest.fixture
def cutoff():
    return 1.0e-5



########################
### HELPER FUNCTIONS ###
########################

def between(series, lo, hi):
    if not (min(series) <= lo):
        raise AssertionError(f"{min(series)} is lower than {lo}")
    elif not (max(series) <= hi):
        raise AssertionError(f"{max(series)} is higher than {hi}")


########################
### POSITIVE TESTS  ###
########################

def test_plank_tset_is_length_3569(plankton) -> None:
    assert len(plankton["Pro"]) == 3659

def test_plank_and_predictors_same_size(plankton, predictors) -> None:
    assert len(plankton["Pro"]) == len(predictors["PO4"])

def test_plankton_tset_contains_7_funct_groups(plankton) -> None:
    assert len(plankton) == 7

def test_predictor_tset_contains_7_columns(predictors) -> None:
    assert len(predictors.columns) == 7

def test_PO4_between_darwin_min_and_max(predictors) -> None:
    assert between(predictors["PO4"].values, 8.5e-5, 2.5) == True

def test_NO3_between_darwin_min_and_max(predictors) -> None:
    assert between(predictors["NO3"].values, 1.2e-8, 35) == True

def test_Fe_between_darwin_min_and_max(predictors) -> None:
    assert between(predictors["Fe"].values, 1.7e-8, 1.1e-3) == True

def test_Si_between_darwin_min_and_max(predictors) -> None:
    assert between(predictors["Si"].values, 3.7e-9, 75) == True

def test_SST_between_ocean_min_and_max(predictors) -> None:
    assert between(predictors["SST"].values, -2.1, 32.3)

def test_SSS_between_ocean_min_and_max(predictors) -> None:
    assert between(predictors["SSS"].values, 1.4, 38)

def test_PAR_between_ocean_min_and_max(predictors) -> None:
    assert between(predictors["PAR"].values, 6.6e-36, 53.8)

def test_min_plankton_biomass_equal_or_greater_than_cutoff(plankton, cutoff) -> None:
    plank = TrainGams.apply_cutoff(cutoff, plankton)
    assert min(plank[0]["Pro"]) >= cutoff
    assert min(plank[0]["Pico"]) >= cutoff
    assert min(plank[0]["Cocco"]) >= cutoff
    assert min(plank[0]["Diazo"]) >= cutoff
    assert min(plank[0]["Diatom"]) >= cutoff
    assert min(plank[0]["Dino"]) >= cutoff
    assert min(plank[0]["Zoo"]) >= cutoff



