from datetime import datetime

"""
    This class defines the current transaction. This class allows everything related to the preview of the receipt and also the finalization of the current session.This class interacts with the GUI.
    Its attributes are:
        - Cart element, modified by the GUI.
        - Global inventory
        - Member Status, verified by the button in the GUI
        - Transaction ID
        - Current date
        - Sub total, total before any tax
        - Tax total, the overall cost of the tax
        - Total, the overall total
        - Cash, the ammount of currency the user has used to pay. Modified by GUI. 
        - Change, the ammount of currency to be returned. 
    
"""


class Transaction:
    def __init__(self, inventory, cart, is_member, transaction_id):
        self.cart = cart
        self.inventory = inventory
        self.is_member = is_member
        self.transaction_id = transaction_id
        self.date = datetime.now()
        self.sub_total = self.calculate_sub_total()
        self.tax = self.calculate_tax()
        self.total = self.sub_total + self.tax
        self.cash = 0
        self.change = 0

    # ***** FUNCTIONS ***** #
    def calculate_sub_total(self):
        """Calculate the sub-total of all items in the cart."""
        sub_total = 0
        for item in self.cart.items.values():
            sub_total += item.get_total_price(self.is_member)
        return sub_total

    def calculate_tax(self):
        """Calculate the total tax for all taxable items in the cart."""
        tax = 0
        tax_rate = 0.065
        for item in self.cart.items.values():
            if item.product.tax_status == "Taxable":
                tax += item.get_total_price(self.is_member) * tax_rate
        return tax

    def generate_receipt(self, cash):
        """Generate a formatted receipt for the transaction."""
        if cash == 0.0:
            self.set_cash_received(100.00)
        else:
            self.set_cash_received(cash)
        spacing = 20
        whitespace_string = " " * spacing
        item_length = len("Item")
        quantity_length = len("Quantity")
        unit_price_length = len("Unitary")
        total_length = len("Total")
        items_sold = sum(item.quantity for item in self.cart.items.values())
        receipt_lines = [
            self.date.strftime("%B %d, %Y"),
            f"TRANSACTION: {self.transaction_id}",
            f"Item{whitespace_string}Quantity{
                whitespace_string}Unitary{whitespace_string}Total"
        ]
        for item in self.cart.items.values():
            unit_price = item.product.member_price if self.is_member else item.product.regular_price
            total_price = item.get_total_price(self.is_member)

            items_spacing = 20
            quantity_spacing = 20
            unit_price_spacing = 20

            # Conditionals to ensure spacing in the transaction receipt
            if len(item.product.name) <= item_length:
                items_spacing = items_spacing + \
                    (item_length - len(item.product.name))
            else:
                items_spacing = items_spacing - \
                    (len(item.product.name) - item_length)

            if len(str(item.quantity)) <= quantity_length:
                quantity_spacing = quantity_spacing + \
                    (quantity_length - len(str(item.quantity)))
            else:
                quantity_spacing = quantity_spacing - \
                    (len(item.quantity) - quantity_length)

            if len(str(unit_price)) <= unit_price_length:
                unit_price_spacing = unit_price_spacing + \
                    (unit_price_length - len(str(unit_price)))
            else:
                unit_price_spacing = unit_price_spacing - \
                    (len(str(unit_price)) - unit_price_length)

            receipt_lines.append(f"{item.product.name}{items_spacing*" "}{item.quantity}{quantity_spacing*" "}${
                                 unit_price:.2f}{unit_price_spacing*" "}${total_price:.2f}")

        receipt_lines.append("************************************")
        receipt_lines.append(f"TOTAL NUMBER OF ITEMS SOLD: {items_sold}")
        receipt_lines.append(f"SUB-TOTAL: ${self.sub_total:.2f}")
        receipt_lines.append(f"TAX (6.5%): ${self.tax:.2f}")
        receipt_lines.append(f"TOTAL: ${self.total:.2f}")
        receipt_lines.append(f"CASH: ${self.cash:.2f}")
        receipt_lines.append(f"CHANGE: ${self.change:.2f}")

        return "\n".join(receipt_lines)

    def set_cash_received(self, cash):
        """Set the cash received and calculate the change."""
        self.cash = cash
        self.change = cash - self.total

    def finalize(self, cash):
        """Finalize the transaction: update inventory, generate and save the receipt, and clear the cart."""
        for item in self.cart.items.values():
            self.inventory.products[item.product.name].quantity -= item.quantity

        receipt = self.generate_receipt(cash)

        receipt_filename = f"./Transactions/transaction_{
            self.transaction_id}-{self.date.strftime("%d-%m-%Y")}.txt"
        with open(receipt_filename, "w") as file:
            file.write(receipt)
        print(f"Receipt saved to {receipt_filename}")

        self.inventory.save_inventory('./Inventory/inventory.txt')

        self.cart.empty_cart()

        return receipt
