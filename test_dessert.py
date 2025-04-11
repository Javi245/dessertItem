import pytest
from dessert import Candy, Cookie, IceCream, Sundae

@pytest.fixture
def candy():
    return Candy()

@pytest.fixture
def custom_candy():
    return Candy(name="Chocolate", candy_weight=0.5, price_per_pound=5.0)

def test_dessertitem_defaults_via_candy(candy):
    assert candy.name == ""
    assert candy.tax_percent == 7.25

def test_update_tax_percent(custom_candy):
    custom_candy.tax_percent = 8.5
    assert custom_candy.tax_percent == 8.5

def test_candy_packaging(custom_candy):
    assert custom_candy.packaging == "Bag"

def test_dessert_item_relational_operators():
    candy1 = Candy("Chocolate Bar", 1.0, 3.50)  # Cost: $3.50
    candy2 = Candy("Chocolate Bar", 2.0, 3.50)  # Cost: $7.00
    cookie = Cookie("Chocolate Chip", 6, 6.00)  # Cost: $3.00
    
    assert candy1 == Candy("Chocolate Bar", 1.5, 2.00)  # Same name, different cost
    
    assert candy1 != cookie  
    
    
    assert cookie < candy1  # $3.00 < $3.50
    
    
    assert cookie <= candy1  # $3.00 <= $3.50
    assert candy1 <= Candy("Chocolate Bar", 1.0, 3.50)  
    
    
    assert candy2 > candy1  # $7.00 > $3.50
    
    
    assert candy2 >= candy1  # $7.00 >= $3.50
    assert candy1 >= candy1  # Equal to itself