import os
import pytest
from pathlib import Path
import pandas as pd

BASE = Path(os.path.abspath(__file__)).parents[1]
DATA = BASE / "data" / "processed"



plank_tset = pd.read_pickle(f"{DATA}/sampled_plankton/plankton.pkl")
pred_tset = pd.read_pickle(f"{DATA}/sampled_predictors/predictors.pkl")
cutoff = 1.001e-5



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

def test_plank_tset_is_length_3569(plank_tset) -> None:
    assert len(plank_tset[0]) == 3569

def test_plank_and_pred_tset_same_size(plank_tset, pred_tset) -> None:
    assert len(plank_tset[0]) == len(pred_tset[0])

def test_plank_tset_contains_7_funct_groups(plank_tset) -> None:
    pass

def test_pred_tset_contains_7_columns(pred_tset) -> None:
    pass

def test_PO4_between_darwin_min_and_max(pred_tset) -> None:
    assert between(pred_tset["PO4"].values, 6e-5, 2.5) == True

def test_NO3_between_darwin_min_and_max(pred_tset) -> None:
    assert between(pred_tset["NO3"].values, 1.2e-8, 35) == True

def test_Fe_between_darwin_min_and_max(pred_tset) -> None:
    assert between(pred_tset["Fe"].values, 1.7e-8, 1.1e-3) == True

def test_Si_between_darwin_min_and_max(pred_tset) -> None:
    assert between(pred_tset["Si"].values, 3.7e-9, 75) == True

def test_SST_between_ocean_min_and_max(pred_tset) -> None:
    assert between(pred_tset["SST"].values, -2.1, 32.3)

def test_SSS_between_ocean_min_and_max(pred_tset) -> None:
    assert between(pred_tset["SSS"].values, 1.4, 38)

def test_PAR_between_ocean_min_and_max(pred_tset) -> None:
    assert between(pred_tset["PAR"].values, 6.6e-36, 53.8)

def test_min_plankton_biomass_equal_or_greater_than_cutoff(pred_tset) -> None:
    assert min(pred_tset["Pro"]) >= cutoff
    assert min(pred_tset["Pico"]) >= cutoff
    assert min(pred_tset["Cocco"]) >= cutoff
    assert min(pred_tset["Diazo"]) >= cutoff
    assert min(pred_tset["Diatom"]) >= cutoff
    assert min(pred_tset["Dino"]) >= cutoff
    assert min(pred_tset["Zoo"]) >= cutoff



