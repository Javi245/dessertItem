import pytest
from dessert import IceCream


@pytest.fixture
def ice_cream():
    return IceCream()


@pytest.fixture
def custom_ice_cream():
    return IceCream(name="Vanilla", scoop_count=2, price_per_scoop=3.0)


def test_ice_cream_defaults(ice_cream):
    assert ice_cream.name == ""
    assert ice_cream.scoop_count == 0
    assert ice_cream.price_per_scoop == 0.0


def test_custom_ice_cream(custom_ice_cream):
    assert custom_ice_cream.name == "Vanilla"
    assert custom_ice_cream.scoop_count == 2
    assert custom_ice_cream.price_per_scoop == 3.0


def test_ice_cream_calculate_cost(custom_ice_cream):
    expected_cost = round(2 * 3.0, 2)
    assert custom_ice_cream.calculate_cost() == expected_cost


def test_ice_cream_calculate_tax(custom_ice_cream):
    cost = custom_ice_cream.calculate_cost()
    expected_tax = round(cost * (custom_ice_cream.tax_percent / 100), 2)
    assert custom_ice_cream.calculate_tax() == expected_tax


def test_ice_cream_packaging(custom_ice_cream):
    assert custom_ice_cream.packaging == "Bowl"