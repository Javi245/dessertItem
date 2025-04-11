from typing import Literal, Dict
from dessert import Candy, Cookie, IceCream, Sundae, Order
from tabulate import tabulate
from payable import PayType

class DessertShop:
    def prompt_customer_name(self):
        while True:
            customer_name = input("Enter customer name: ")
            if not customer_name:
                print("Name cannot be empty.")
                continue
            return customer_name
    def user_prompt_candy(self):
        while True:
            name = input("Enter the name of candy: ")
            if not name:
                print("Name cannot be empty.")
                continue
            try:
                weight = input("Enter weight(lbs): ")
                weight = float(weight)
                if weight <= 0:
                    print("Weight must be greater than 0.")
                    continue
            except ValueError:
                print("Weight must be a number.")
                continue
            try:
                price = input("Enter price per pound: ")
                price = float(price)
                if price <= 0:
                    print("Price must be greater than 0.")
                    continue
            except ValueError:
                print("Price must be a number.")
                continue
            return Candy(name, weight, price)

    def user_prompt_cookie(self):
        while True:
            name = input("Enter the type of cookie: ")
            if not name:
                print("Name cannot be empty.")
                continue
            try:
                quantity = input("Enter the quantity purchased: ")
                quantity = int(quantity)
                if quantity <= 0:
                    print("Quantity must be greater than 0.")
                    continue
            except ValueError:
                print("Quantity must be a number.")
                continue
            try:
                price = input("Enter the price per dozen: ")
                price = float(price)
                if price <= 0:
                    print("Price must be greater than 0.")
                    continue
            except ValueError:
                print("Price must be a number.")
                continue
            return Cookie(name, quantity, price)

    def user_prompt_icecream(self):
        while True:
            name = input("Enter the type of ice cream: ")
            if not name:
                print("Name cannot be empty.")
                continue
            try:
                scoops = input("Enter the number of scoops: ")
                scoops = int(scoops)
                if scoops <= 0:
                    print("Scoops must be greater than 0.")
                    continue
            except ValueError:
                print("Scoops must be a number.")
                continue
            try:
                price = input("Enter the price per scoop: ")
                price = float(price)
                if price <= 0:
                    print("Price must be greater than 0.")
                    continue
            except ValueError:
                print("Price must be a number.")
                continue
            return IceCream(name, scoops, price)

    def user_prompt_sundae(self):
        while True:
            name = input("Enter the type of ice cream: ")
            if not name:
                print("Name cannot be empty.")
                continue
            try:
                scoops = input("Enter the number of scoops: ")
                scoops = int(scoops)
                if scoops <= 0:
                    print("Scoops must be greater than 0.")
                    continue
            except ValueError:
                print("Scoops must be a number.")
                continue
            try:
                price = input("Enter the price per scoop: ")
                price = float(price)
                if price <= 0:
                    print("Price must be greater than 0.")
                    continue
            except ValueError:
                print("Price must be a number.")
                continue
            try:
                topping = input("Enter the kind of topping used: ")
                if not topping:
                    print("Topping cannot be empty.")
                    continue
            except ValueError:
                print("Topping must be a string.")
                continue
            try:
                topping_price = input("Enter the price for the topping: ")
                topping_price = float(topping_price)
                if topping_price <= 0:
                    print("Price must be greater than 0.")
                    continue
            except ValueError:
                print("Price must be a number.")
                continue
            return Sundae(name, scoops, price, topping, topping_price)

    def payment_type(self) -> str:
        """
        Prompts the user to select a payment type and validates it.
        Returns a valid payment type or raises ValueError.
        """
        try:
            payment_method = int(input("1:CASH" + "\n" + "2:CARD" + "\n" + "3:PHONE" + "\n" + "Enter payment method): ").strip())
        
            if payment_method == 1:
                payment_method = "CASH"
                return payment_method
            elif payment_method == 2:
                payment_method = "CARD"
                return payment_method
            elif payment_method == 3:
                payment_method = "PHONE"
                return payment_method
            else:
                raise ValueError("The payment method entered is not valid. Please try again.")

        except ValueError as e:
            print(f"Error: {e}")
            print("Defaulting to CASH.")
            payment_method = "CASH"
            return payment_method


class Customer:
    id_counter: int = 0
    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.order_history: list[Order] = []
        Customer.id_counter += 1
        self.customer_id = Customer.id_counter

    def add2history(self, order:Order) -> "Customer":
        self.order_history.append(order)
        return self
    
    

customer_db: Dict[str, Customer] = {}

def main():
    while True:
        main_menu: str = "\n".join(
            [
                "1: Start a new order",
                "2: Admin Module",
                "",
                "What would you like to do? (1-2, Enter for done): ",
            ]
        )
        ans = input(main_menu)
        if ans not in ["1", "2"]:
            return
        elif ans == "1":
            global customer_db
            shop = DessertShop()
            order: Order = Order()
            done: bool = False
            prompt = "\n".join(
                [
                    "\n",
                    "1: Candy",
                    "2: Cookie",
                    "3: Ice Cream",
                    "4: Sunday",
                    "\nWhat would you like to add to the order? (1-4, Enter for done): ",
                ]
            )
            while not done:
                choice = input(prompt)
                match choice:
                    case "":
                        done = True
                    case "1":
                        item = shop.user_prompt_candy()
                        order.add(item)
                        print(f"{item.name} has been added to your order.")
                    case "2":
                        item = shop.user_prompt_cookie()
                        order.add(item)
                        print(f"{item.name} has been added to your order.")
                    case "3":
                        item = shop.user_prompt_icecream()
                        order.add(item)
                        print(f"{item.name} has been added to your order.")
                    case "4":
                        item = shop.user_prompt_sundae()
                        order.add(item)
                        print(f"{item.name} has been added to your order.")
                    case _:
                        print(
                            "Invalid response:  Please enter a choice from the menu (1-4) or Enter"
                        )
            print()
            customer_name = shop.prompt_customer_name()
            if customer_name not in customer_db.keys():
                customer = Customer(customer_name)
                customer_db[customer_name] = customer
            else:
                customer = customer_db[customer_name]
            customer_db[customer_name].add2history(order)

            order.sort()
            payment_method = shop.payment_type()
            try:
                order.set_pay_type(payment_method)
            except ValueError as e:
                print(f"Error: {e}")
                print("Defaulting to CASH.")
                order.set_pay_type("CASH")
            print(f"Customer Name: {customer_name}      Customer ID: {customer.customer_id}  Total Order: {len(customer.order_history)}")
            print(tabulate(order.to_list(), tablefmt="fsql"))
            print()
            
        elif ans == "2":
            admin_done = False
            while not admin_done:
                admin_menu = "\n".join([
                    "",
                    "1: Shop Customer List",
                    "2: Customer Order History",
                    "3: Exit Admin Module",
                    "What would you like to do? (1-3): ",
                ])
                admin_choice = input(admin_menu)
                if admin_choice == "1":
                    print()
                    for name, customer_obj in customer_db.items():
                        print(f"Customer Name: {name:<10} Customer ID: {customer_obj.customer_id}")
                elif admin_choice == "2":
                    customer_name = input("Enter the name of the customer: ")
                    try:

                        customer = customer_db[customer_name]
                        print(f"Customer Name: {customer_name}\t Customer ID: {customer.customer_id}")
                        for i, item in enumerate(customer.order_history, start=1):
                            print(f"Order #{i}:")
                            print(tabulate(item.to_list(), tablefmt="fsql"))
                    except Exception as e:
                        print(f"Error: {e}")

                elif admin_choice == "3":
                    admin_done = True

                else:
                    raise ValueError("Invalid response:  Please enter a choice from the menu (1-3) or Enter")






                

if __name__ == "__main__":
    main()
