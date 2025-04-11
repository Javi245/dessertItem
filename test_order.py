from dessert import Order, Candy, Cookie, IceCream
from payable import PayType
import pytest


@pytest.fixture
def order():
    return Order()
    
def test_cash_order(order):
    order.set_pay_type("CASH")
    payment_method = order.get_pay_type()
    assert payment_method == "CASH"

def test_card_order(order):
    order.set_pay_type("CARD")
    assert order.get_pay_type() == "CARD"

def test_phone_order(order):
    order.set_pay_type("PHONE")
    assert order.get_pay_type() == "PHONE"
    
def test_invalid_payment_type(order):
    with pytest.raises(ValueError):
        order.set_pay_type("Invalid type here")

def test_invalid_payment_type_get(order):
    order._payment_method = "Invalid type here"
    with pytest.raises(ValueError):
        order.get_pay_type()

def test_order_sort(order):
    
    # Add items in random cost order
    candy = Candy("Chocolate Bar", 2.0, 3.50)       
    cookie = Cookie("Chocolate Chip", 6, 6.00)       
    ice_cream = IceCream("Vanilla", 3, 1.50)         
    
    order.add(candy)      
    order.add(cookie)     
    order.add(ice_cream)  
    
    # Sort the order
    order.sort()
    
    assert order.order[0] == cookie    
    assert order.order[1] == ice_cream  
    assert order.order[2] == candy     

def test_order_iter_(order):
    candy = Candy("Chocolate Bar", 2.0, 3.50)
    cookie = Cookie("Chocolate Chip", 6, 6.00)
    ice_cream = IceCream("Vanilla", 3, 1.50)
    order.add(candy)
    order.add(cookie)
    order.add(ice_cream)
    items = list(order)
    assert len(items) == 3
    assert items[0] == order.order[0]
    assert items[1] == order.order[1]
    assert items[2] == order.order[2]

def test_order_next_(order):
    candy = Candy("Chocolate Bar", 2.0, 3.50)
    cookie = Cookie("Chocolate Chip", 6, 6.00)
    ice_cream = IceCream("Vanilla", 3, 1.50)
    order.add(candy) 
    order.add(cookie)
    order.add(ice_cream)
    iterator = iter(order)
    first_item = next(iterator)
    assert first_item == order.order[0]
    
    second_item = next(iterator)
    assert second_item == order.order[1]
    
    third_item = next(iterator)
    assert third_item == order.order[2]
    
    with pytest.raises(StopIteration):
        next(iterator) 


