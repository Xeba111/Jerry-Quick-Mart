from inventory import Inventory
from product import Product

"""
    This class defines CartItem, a class that stores Products and its quantity. 
    Its attributes are:
        - Product element
        - Quantity of the Product
    
    Other attributes from the Product do not need to be stored in this class because that information is already in the Product class itself.
    
"""


class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    # ***** FUNCTIONS *****
    def get_unit_price(self, is_member=False):
        """Get the unit price of a certain product"""
        if is_member:
            return self.product.member_price
        else:
            return self.product.regular_price

    def get_total_price(self, is_member=False):
        """Get the total price of a certain product"""
        if is_member:
            return self.quantity * self.product.member_price
        else:
            return self.quantity * self.product.regular_price
