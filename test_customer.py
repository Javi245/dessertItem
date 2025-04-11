from dessertshop import Customer
from dessert import Order
import pytest


@pytest.fixture
def customer():
    return Customer("Test Customer")


def test_customer_name(customer):
    assert customer.customer_name == "Test Customer"


def test_customer_initial_attributes(customer):
    assert hasattr(customer, 'customer_name')
    assert hasattr(customer, 'customer_id')
    assert hasattr(customer, 'order_history')
    assert isinstance(customer.order_history, list)
    assert len(customer.order_history) == 0


def test_customer_id_unique():
    original_id = Customer.id_counter
    Customer.id_counter = 0

    customer1 = Customer("Customer 1")
    customer2 = Customer("Customer 2")
    customer3 = Customer("Customer 3")

    assert customer1.customer_id == 1
    assert customer2.customer_id == 2
    assert customer3.customer_id == 3

    assert customer1.customer_id != customer2.customer_id
    assert customer1.customer_id != customer3.customer_id
    assert customer2.customer_id != customer3.customer_id

    Customer.id_counter = original_id


def test_add2history_returns_self(customer):
    order = Order()

    returned_customer = customer.add2history(order)
    assert returned_customer is customer