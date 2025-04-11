import pytest
from dessert import Sundae


@pytest.fixture
def sundae():
    return Sundae()


@pytest.fixture
def custom_sundae():
    return Sundae(
        name="Vanilla",
        scoop_count=2,
        price_per_scoop=3.0,
        topping_name="Sprinkles",
        topping_price=0.5,
    )


def test_sundae_defaults(sundae):
    assert sundae.name == ""
    assert sundae.scoop_count == 0
    assert sundae.price_per_scoop == 0.0
    assert sundae.topping_name == ""
    assert sundae.topping_price == 0.0


def test_custom_sundae(custom_sundae):
    assert custom_sundae.name == "Vanilla"
    assert custom_sundae.scoop_count == 2
    assert custom_sundae.price_per_scoop == 3.0
    assert custom_sundae.topping_name == "Sprinkles"
    assert custom_sundae.topping_price == 0.5


def test_sundae_calculate_cost(custom_sundae):
    expected_cost = round((2 * 3.0) + 0.5, 2)
    assert custom_sundae.calculate_cost() == expected_cost


def test_sundae_calculate_tax(custom_sundae):
    cost = custom_sundae.calculate_cost()
    expected_tax = round(cost * (custom_sundae.tax_percent / 100), 2)
    assert custom_sundae.calculate_tax() == expected_tax


def test_sundae_packaging(custom_sundae):
    assert custom_sundae.packaging == "Boat"