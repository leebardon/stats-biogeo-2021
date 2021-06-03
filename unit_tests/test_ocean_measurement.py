import pytest
import pandas as pd
import xarray as xr

import os, sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(".."))

base_path = Path(os.path.abspath(__file__)).parents[1]
OCEAN_OBVS = base_path / "data" / "raw" / "ocean_observations.netcdf"


from src.controllers import OceanMeasurementsController
from src.models.sample_measurements import AddColumns, CleanData, CreateSamplingMatrix


class BasicSamplingMatrixTestCase(TestCase):
    def setUp(self) -> None:
        self.ocean_data = xr.open_dataset(OCEAN_OBVS)

    def tearDown(self) -> None:
        pass


class TestBuildSamplingMatrix(BasicSamplingMatrixTestCase):
    def test_decode_all_columns_should_return_floats(self) -> None:
        pass

    def test_drop_erroneous_should_return_max_year_2008(self) -> None:
        pass

    def test_drop_erroneous_should_return_max_day_996e27(self) -> None:
        pass

    def test_create_months_columns_should_return_year_min_1987(self) -> None:
        pass

    def test_create_months_columns_should_return_year_max_2008(self) -> None:
        pass

    def test_create_months_columns_should_return_months_min_1(self) -> None:
        pass

    def test_create_months_columns_should_return_months_max_264(self) -> None:
        pass
