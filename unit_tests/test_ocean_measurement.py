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

    # def test_


# class TestPostUniversities(BasicUniversityAPITestCase):
#     def test_create_university_without_arguments_should_fail(self) -> None:
#         res = self.client.post(path=self.unis_url)
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(json.loads(res.content), {"name": ["This field is required."]})

#     def test_create_existing_university_should_fail(self) -> None:
#         University.objects.create(name="Southampton")
#         res = self.client.post(path=self.unis_url, data={"name": "Southampton"})
#         self.assertEqual(res.status_code, 400)
#         self.assertEqual(
#             json.loads(res.content),
#             {"name": ["university with this name already exists."]},
#         )

#     def test_create_university_with_name_and_default_fields_only(self) -> None:
#         res = self.client.post(path=self.unis_url, data={"name": "test uni"})
#         response_content = json.loads(res.content)
#         self.assertEqual(res.status_code, 201)
#         self.assertEqual(response_content.get("name"), "test uni")
#         self.assertEqual(response_content.get("status"), "Hiring")
#         self.assertEqual(response_content.get("application_link"), "")
#         self.assertEqual(response_content.get("notes"), "")

#     def test_create_uni_with_layoffs_status_should_succeed(self) -> None:
#         res = self.client.post(
#             path=self.unis_url, data={"name": "test uni", "status": "Layoffs"}
#         )
#         self.assertEqual(res.status_code, 201)
#         res_content = json.loads(res.content)
#         self.assertEqual(res_content.get("status"), "Layoffs")

#     def test_create_uni_with_wrong_status_should_fail(self) -> None:
#         res = self.client.post(
#             path=self.unis_url, data={"name": "test uni", "status": "VeryWrongIndeed"}
#         )
#         self.assertEqual(res.status_code, 400)
#         res_content = json.loads(res.content)
#         self.assertIn("VeryWrongIndeed", str(res.content))
#         self.assertIn("is not a valid choice", str(res.content))
