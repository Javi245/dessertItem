from typing import Protocol, Literal

PayType = Literal["CASH", "CARD", "PHONE"]

class Payable(Protocol):
    def get_pay_type(self) -> PayType:
        """Return the current payment method."""
        ...
    
    def set_pay_type(self, payment_method: PayType) -> None:
        """Set the payment method."""
        ...