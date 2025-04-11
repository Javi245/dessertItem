import pytest
from dessert import Cookie


@pytest.fixture
def cookie():
    return Cookie()


@pytest.fixture
def custom_cookie():
    return Cookie(name="Chocolate Chip", cookie_quantity=12, price_per_dozen=10.0)


def test_cookie_defaults(cookie):
    assert cookie.name == ""
    assert cookie.cookie_quantity == 0
    assert cookie.price_per_dozen == 0.0


def test_custom_cookie(custom_cookie):
    assert custom_cookie.name == "Chocolate Chip"
    assert custom_cookie.cookie_quantity == 12
    assert custom_cookie.price_per_dozen == 10.0


def test_cookie_calculate_cost(custom_cookie):
    expected_cost = round(1 * 10.0, 2)
    assert custom_cookie.calculate_cost() == expected_cost


def test_cookie_calculate_tax(custom_cookie):
    cost = custom_cookie.calculate_cost()
    expected_tax = round(cost * (custom_cookie.tax_percent / 100), 2)
    assert custom_cookie.calculate_tax() == expected_tax


def test_cookie_packaging(custom_cookie):
    assert custom_cookie.packaging == "Box"

    
def test_can_combine():
    cookie1 = Cookie(name="Chocolate Chip", cookie_quantity=12, price_per_dozen=10.0)
    cookie2 = Cookie(name="Chocolate Chip", cookie_quantity=24, price_per_dozen=10.0)
    assert cookie1.can_combine(cookie2) is True


def test_cannot_combine_different_name():
    cookie1 = Cookie(name="Chocolate Chip", cookie_quantity=12, price_per_dozen=10.0)
    cookie2 = Cookie(name="Oatmeal Raisin", cookie_quantity=24, price_per_dozen=10.0)
    assert cookie1.can_combine(cookie2) is False


def test_different_price():
    cookie1 = Cookie(name="Chocolate Chip", cookie_quantity=12, price_per_dozen=10.0)
    cookie2 = Cookie(name="Chocolate Chip", cookie_quantity=24, price_per_dozen=12.0)
    assert cookie1.can_combine(cookie2) is False


def test_not_cookie():
    not_cookie = "not a cookie"
    cookie1 = Cookie(name="Chocolate Chip", cookie_quantity=12, price_per_dozen=10.0)
    assert cookie1.can_combine(not_cookie) is False


def test_combine_cookies():
    cookie1 = Cookie(name="Chocolate Chip", cookie_quantity=12, price_per_dozen=10.0)
    cookie2 = Cookie(name="Chocolate Chip", cookie_quantity=24, price_per_dozen=10.0)
    
    result = cookie1.combine(cookie2)
    assert cookie1.cookie_quantity == 36
    assert cookie1.name == "Chocolate Chip"
    assert cookie1.price_per_dozen == 10.0
    assert result is cookie1


def test_combine_different_cookies():
    cookie1 = Cookie(name="Chocolate Chip", cookie_quantity=12, price_per_dozen=10.0)
    not_cookie = "not a cookie"
    
    with pytest.raises(TypeError):
        cookie1.combine(not_cookie)


