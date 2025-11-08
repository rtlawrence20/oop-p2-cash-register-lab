#!/usr/bin/env python3


class CashRegister:
    """A cash register that can add items, apply a percentage discount,
    and void the last transaction.
    """

    def __init__(self, discount=0):
        # initialize tracked state
        self._discount = 0
        self.discount = discount
        self.total = 0
        self.items = []
        self.previous_transactions = []

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        try:
            ivalue = int(value)
        except (TypeError, ValueError):
            print("Not valid discount")
            self._discount = 0
            return
        if 0 <= ivalue <= 100:
            self._discount = ivalue
        else:
            print("Not valid discount")
            self._discount = 0

    def add_item(self, item, price, quantity=1):
        """Add an item (optionally with quantity) to the register.
        Increases the total and records items and a transaction so it can be voided later.
        """
        qty = int(quantity) if quantity is not None else 1
        subtotal = float(price) * qty

        # update total
        self.total += subtotal

        # extend items list
        self.items.extend([item] * qty)

        # push transaction on stack
        self.previous_transactions.append(
            {
                "item": item,
                "price": float(price),
                "quantity": qty,
                "subtotal": subtotal,
            }
        )

    def apply_discount(self):
        """Apply the stored percentage discount to the current total.
        Prints message.
        """
        if not self.discount:
            print("There is no discount to apply.")
            return

        # Apply percentage off
        discounted_total = self.total * (100 - self.discount) / 100.0
        self.total = discounted_total

        # printing format: if integer, print without decimals
        if self.total.is_integer():
            shown = str(int(self.total))
        else:
            shown = f"{self.total:.2f}".rstrip("0").rstrip(".")
        print(f"After the discount, the total comes to ${shown}.")

    def void_last_transaction(self):
        """Remove the last transaction's impact from total (and items list)."""
        if not self.previous_transactions:
            self.total = 0.0
            return

        tx = self.previous_transactions.pop()
        self.total -= tx["subtotal"]
        if abs(self.total) < 1e-12:
            self.total = 0.0

        # remove the last 'quantity' items from items list
        qty = tx["quantity"]
        for _ in range(min(qty, len(self.items))):
            self.items.pop()
