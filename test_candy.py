import pytest
from dessert import Candy


@pytest.fixture
def candy():
    return Candy()


@pytest.fixture
def custom_candy():
    return Candy(name="Chocolate", candy_weight=0.5, price_per_pound=5.0)


def test_candy_defaults(custom_candy):
    assert custom_candy.name == "Chocolate"
    assert custom_candy.candy_weight == 0.5
    assert custom_candy.price_per_pound == 5.0


def test_candy_calculate_cost(custom_candy):
    expected_cost = round(0.5 * 5.0, 2)
    assert custom_candy.calculate_cost() == expected_cost


def test_candy_calculate_tax(custom_candy):
    cost = custom_candy.calculate_cost()
    expected_tax = round(cost * (custom_candy.tax_percent / 100), 2)
    assert custom_candy.calculate_tax() == expected_tax
    
def test_candy_packaging(custom_candy):
    assert custom_candy.packaging == "Bag"
    
def test_candy_can_combine_same_name_and_price():
    candy1 = Candy(name="Chocolate", candy_weight = 0.5, price_per_pound = 5.0)
    candy2 = Candy(name="Chocolate", candy_weight=0.5, price_per_pound=5.0)
    assert candy1.can_combine(candy2) is True

def test_candy_can_combine_different_name():
    candy1 = Candy(name="Chocolate", candy_weight=0.5, price_per_pound=5.0)
    candy2 = Candy(name="Chocolate", candy_weight=0.5, price_per_pound=6.0)
    assert candy1.can_combine(candy2) is False

def test_candy_can_combine_different_names_same_price():
    candy1 = Candy(name="Vanilla", candy_weight=0.5, price_per_pound=5.0)
    candy2 = Candy(name="Chocolate", candy_weight=0.5, price_per_pound=5.0)
    assert candy1.can_combine(candy2) is False

def test_candy_can_combine_not_candy():
    not_candy = "not a candy"
    candy1 = Candy(name="Vanilla", candy_weight=0.5, price_per_pound=5.0)
    assert candy1.can_combine(not_candy) is False

def test_candy_combine_candies():
    candy1 = Candy(name="Vanilla", candy_weight=0.5, price_per_pound=5.0)
    candy2 = Candy(name="Vanilla", candy_weight=0.75, price_per_pound=5.0)

    result = candy1.combine(candy2)
    assert candy1.candy_weight == 0.75 + 0.5
    assert candy1.name == "Vanilla"
    assert candy1.price_per_pound == 5.0
    assert result is candy1

def test_combine():
    candy1 = Candy(name="Vanilla", candy_weight=0.5, price_per_pound=5.0)
    not_candy = "not a candy"
    with pytest.raises(TypeError):
        candy1.combine(not_candy)
