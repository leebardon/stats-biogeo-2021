import pytest


@pytest.mark.add_months
def test_add_month_columns():

    assert x + 1 == y, "test failed"
    assert x == y, "test failed because x=" + str(x) + " y=" + str(y)


@pytest.mark.set1
def test_file2_method2():
    x = 5
    y = 6
    assert x + 1 == y, "test failed"
