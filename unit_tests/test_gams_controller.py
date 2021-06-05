import os
import pytest
import unittest
from pathlib import Path
from unittest import TestCase
import pandas as pd

BASEPATH = Path(os.path.abspath(__file__)).parents[1]
DATA = BASEPATH / "data" / "processed"


class BasicGamsTestCase(TestCase):
    def setUp(self) -> None:
        self.plank_tset = pd.read_pickle(f"{DATA}/sampled_plankton/plankton.pkl")
        self.pred_tset = pd.read_pickle(f"{DATA}/sampled_predictors/predictors.pkl")
        self.cutoff = 1.001e-5

    def tearDown(self) -> None:
        pass


class BetweenAssertMixin(object):
    def assertBetween(series, lo, hi):
        if not (min(series) <= lo):
            raise AssertionError(f"{min(series)} is lower than {lo}")
        elif not (max(series) <= hi):
            raise AssertionError(f"{max(series)} is higher than {hi}")


class TestLoadedTrainingSets(BasicGamsTestCase, BetweenAssertMixin):
    def test_plank_tset_is_length_3569(self) -> None:
        assertEqual(len(self.plank_tset[0]), 3569)

    def test_plank_and_pred_tset_same_size(self) -> None:
        assertEqual(len(self.plank_tset[0]), len(self.pred_tset[0]))

    def test_plank_tset_contains_7_funct_groups(self) -> None:
        pass

    def test_pred_tset_contains_7_columns(self) -> None:
        pass

    def test_PO4_between_darwin_min_and_max(self) -> None:
        self.assertBetween(self.pred_tset["PO4"].values, 6e-5, 2.5)

    def test_NO3_between_darwin_min_and_max(self) -> None:
        self.assertBetween(self.pred_tset["NO3"].values, 1.2e-8, 35)

    def test_Fe_between_darwin_min_and_max(self) -> None:
        self.assertBetween(self.pred_tset["Fe"].values, 1.7e-8, 1.1e-3)

    def test_Si_between_darwin_min_and_max(self) -> None:
        self.assertBetween(self.pred_tset["Si"].values, 3.7e-9, 75)

    def test_SST_between_ocean_min_and_max(self) -> None:
        debugger()
        self.assertBetween(self.pred_tset["SST"].values, -2.1, 32.3)

    def test_SSS_between_ocean_min_and_max(self) -> None:
        self.assertBetween(self.pred_tset["SSS"].values, 1.4, 38)

    def test_PAR_between_ocean_min_and_max(self) -> None:
        self.assertBetween(self.pred_tset["PAR"].values, 6.6e-36, 53.8)


class TestGams(BasicGamsTestCase):
    def test_min_pro_biomass_equal_or_greater_than_cutoff(self) -> None:
        assertTrue(min(self.pred_tset["Pro"]) >= self.cutoff)

    def test_min_pico_biomass_equal_or_greater_than_cutoff(self) -> None:
        assertTrue(min(self.pred_tset["Pico"]) >= self.cutoff)

    def test_min_cocco_biomass_equal_or_greater_than_cutoff(self) -> None:
        assertTrue(min(self.pred_tset["Cocco"]) >= self.cutoff)

    def test_min_diazo_biomass_equal_or_greater_than_cutoff(self) -> None:
        assertTrue(min(self.pred_tset["Diazo"]) >= self.cutoff)

    def test_min_diatom_biomass_equal_or_greater_than_cutoff(self) -> None:
        assertTrue(min(self.pred_tset["Diatom"]) >= self.cutoff)

    def test_min_dino_biomass_equal_or_greater_than_cutoff(self) -> None:
        assertTrue(min(self.pred_tset["Dino"]) >= self.cutoff)

    def test_min_zoo_biomass_equal_or_greater_than_cutoff(self) -> None:
        assertTrue(min(self.pred_tset["Zoo"]) >= self.cutoff)
