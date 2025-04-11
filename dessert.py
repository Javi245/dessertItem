from abc import ABC, abstractmethod
from packaging import Packaging
from payable import Payable, PayType
from typing import List, TYPE_CHECKING
from combine import Combinable  # Import Combinable protocol


class DessertItem(ABC, Packaging):
    def __init__(self, name="", tax_percent: float = 7.25, packaging=None):
        self.name = name
        self.tax_percent = tax_percent
        self.packaging = packaging

    @abstractmethod
    def calculate_cost(self) -> float:
        pass

    def calculate_tax(self) -> float:
        return round(self.calculate_cost() * (self.tax_percent / 100), 2)

    def __eq__(self, other):
        if isinstance(other, DessertItem):
            return self.name == other.name
        return False
    
    def __ne__(self, value):
        if isinstance(value, DessertItem):
            return self.name != value.name
        return True
    
    def __lt__(self, other):
        if isinstance(other, DessertItem):
            return self.calculate_cost() < other.calculate_cost()
        return False
    
    def __le__(self, other):
        if isinstance(other, DessertItem):
            return self.calculate_cost() <= other.calculate_cost()
        return False
    
    def __gt__(self, other):
        if isinstance(other, DessertItem):
            return self.calculate_cost() > other.calculate_cost()
        return False
    
    def __ge__(self, other):
        if isinstance(other, DessertItem):
            return self.calculate_cost() >= other.calculate_cost()
        return False
    


class Candy(DessertItem):
    def __init__(self, name="", candy_weight=0.0, price_per_pound=0.0, packaging=None):
        super().__init__(name, packaging="Bag" if packaging is None else packaging)
        self.candy_weight = candy_weight
        self.price_per_pound = price_per_pound

    def calculate_cost(self):
        return round(self.candy_weight * self.price_per_pound, 2)

    def __str__(self):
        return (
            f"{self.name} ({self.packaging})\n"
            f"-    {self.candy_weight} lbs. @ ${self.price_per_pound}/lb:             ${self.calculate_cost():.2f}   [Tax: ${self.calculate_tax():.2f}]"
        )
    
    def can_combine(self, other) -> bool:
        """
        Check if this candy can be combined with another candy.
        Returns True only if the other object is a Candy with the same name and price_per_pound.
        """
        if not isinstance(other, Candy):
            return False
        return (self.name == other.name and 
                self.price_per_pound == other.price_per_pound)
    
    def combine(self, other:"Candy") -> 'Candy':
        if not isinstance(other, Candy):
            raise TypeError("Not an instance of Candy")
        self.candy_weight += other.candy_weight
        return self
    
class Cookie(DessertItem):
    def __init__(self, name="", cookie_quantity=0, price_per_dozen=0.0, packaging=None):
        super().__init__(name, packaging="Box" if packaging is None else packaging)
        self.cookie_quantity = cookie_quantity
        self.price_per_dozen = price_per_dozen

    def calculate_cost(self):
        dozens = self.cookie_quantity / 12
        return round(dozens * self.price_per_dozen, 2)

    def __str__(self):
        full_name = self.name if "Cookies" in self.name else f"{self.name} Cookies"
        return (
            f"{full_name} ({self.packaging})\n"
            f"-    {self.cookie_quantity} cookies. @ ${self.price_per_dozen}/dozen:        ${self.calculate_cost():.2f}   [Tax: ${self.calculate_tax():.2f}]"
        )
    
    def can_combine(self, other:"Cookie") -> bool:
        if not isinstance(other, Cookie):
            return False
        return (self.name == other.name and 
                self.price_per_dozen == other.price_per_dozen)
    
    def combine(self, other: "Cookie") -> "Cookie":
        if not isinstance(other, Cookie):
            raise TypeError("Not an instance of Cookie")
        self.cookie_quantity += other.cookie_quantity
        return self
        

class IceCream(DessertItem):
    def __init__(self, name="", scoop_count=0, price_per_scoop=0.0, packaging=None):
        super().__init__(name, packaging="Bowl" if packaging is None else packaging)
        self.scoop_count = scoop_count
        self.price_per_scoop = price_per_scoop

    def calculate_cost(self):
        return round(self.scoop_count * self.price_per_scoop, 2)

    def __str__(self):
        return (
            f"{self.name} Ice Cream ({self.packaging})\n"
            f"-    {self.scoop_count} scoops. @ ${self.price_per_scoop}/scoop:         ${self.calculate_cost():.2f}   [Tax: ${self.calculate_tax():.2f}]"
        )


class Sundae(IceCream):
    def __init__(
        self,
        name="",
        scoop_count=0,
        price_per_scoop=0.0,
        topping_name="",
        topping_price=0.0,
        packaging=None,
    ):
        
        super().__init__(name, scoop_count, price_per_scoop, packaging="Boat" if packaging is None else packaging)
        self.topping_name = topping_name
        self.topping_price = topping_price

    def calculate_cost(self):
        return round((self.scoop_count * self.price_per_scoop) + self.topping_price, 2)

    def __str__(self):
        return (
            f"{self.topping_name} {self.name} Sundae ({self.packaging})\n"
            f"-    {self.scoop_count} scoops. @ ${self.price_per_scoop}/scoop\n"
            f"-    {self.topping_name} topping @ ${self.topping_price}:            ${self.calculate_cost():.2f}   [Tax: ${self.calculate_tax():.2f}]"
        )


class Order(Payable):
    def __init__(self):
        self.order: List[DessertItem] = []
        self._payment_method: PayType = "CASH"
        self._index = 0
    
    def __iter__(self):
        self._index = 0
        return self
    
    def __next__(self):
        if self._index < len(self.order):
            item = self.order[self._index]
            self._index += 1
            return item
        raise StopIteration
    
    
    def add(self, item):
        if not isinstance(item, Combinable):
            self.order.append(item)
            return
            
        for i, existing_item in enumerate(self.order):
            if isinstance(existing_item, Combinable) and existing_item.can_combine(item):
                self.order[i] = existing_item.combine(item)
                return
                
        self.order.append(item)
    
    def sort(self) -> 'Order':
        self.order.sort() 
        return self
    
    def get_pay_type(self) -> PayType:
        if self._payment_method not in ["CASH", "CARD", "PHONE"]:
            raise ValueError(f"Invalid payment method: {self._payment_method}")
        return self._payment_method
    
    def set_pay_type(self, payment_method: PayType) -> None:
        """Set the payment method."""
        if payment_method not in ["CASH", "CARD", "PHONE"]:
            raise ValueError(f"Invalid payment method: {payment_method}")
        self._payment_method = payment_method

    def __str__(self):
        result = []
        for item in self.order:
            result.append(str(item))
        result.append("--------------------")

        result.append(f"Total number of items in order:       {len(self.order)}")

        subtotal = f"${self.order_cost():.2f}"
        tax = f"[Tax: ${self.order_tax():.2f}]"
        result.append(f"Order Subtotals:                      {subtotal}  {tax}")

        total = f"${self.order_cost() + self.order_tax():.2f}"
        result.append(f"Order Total:                                 {total}")
        
        result.append("--------------------")
        result.append(f"Paid with {self.get_pay_type()}")
        return "\n".join(result)

    def __len__(self):
        return len(self.order)

    def to_list(self):
        result = []
        lines = str(self).split("\n")
        for line in lines:
            if "Total number of items in order" in line:
                parts = line.split(":")
                result.append([parts[0] + ":", parts[1].strip(), ""])
            elif "Order Total" in line:
                parts = line.split("$")
                result.append([parts[0].strip(), "", "$" + parts[1].strip()])
            elif "Payment Method" in line:
                parts = line.split(":")
                result.append([parts[0] + ":", parts[1].strip(), ""])
            else:
                try:
                    before_tax = line.split("[Tax:")[0]
                    item_desc = before_tax.rsplit("$", 1)[0]
                    cost = "$" + before_tax.rsplit("$", 1)[1].strip()
                    tax = "[Tax:" + line.split("[Tax:")[1]
                    result.append([item_desc, cost, tax])
                except (IndexError, ValueError):
                    result.append([line, "", ""])
        return result

    def order_cost(self) -> float:
        return round(sum(item.calculate_cost() for item in self.order), 2)

    def order_tax(self) -> float:
        return round(sum(item.calculate_tax() for item in self.order), 2)