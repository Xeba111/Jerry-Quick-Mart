"""
    This class defines the most basic of Objects in this project: a Product
        Its attributes are:
        - Name
        - Quantity
        - Regular Price
        - Member Price
        - Tax Status
"""


class Product:
    def __init__(self, name, quantity, regular_price, member_price, tax_status):
        self.name = str(name)
        self.quantity = int(quantity)
        self.regular_price = float(regular_price)
        self.member_price = float(member_price)
        self.tax_status = tax_status

    # ***** FUNCTIONS ***** #
    def get_price(self, is_member):
        """Return the price of the product based on customer type."""
        return self.member_price if is_member else self.regular_price
