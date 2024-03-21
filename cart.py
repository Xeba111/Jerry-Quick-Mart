from inventory import Inventory
from product import Product
from cart_item import CartItem


"""
    This class defines the current sessions Cart object. The Cart contains which CartItems the user is currently buying.
    Its attributes are:
         Dictionary to store CartItems. The key is the Product name.
    
"""


class Cart:
    def __init__(self):
        self.items = {}

    # ***** FUNCTIONS ***** #
    def add_item(self, product, quantity):
        """Add a product to the cart or update the quantity if it already exists."""
        if product.name in self.items:
            self.items[product.name].quantity += quantity
        else:
            self.items[product.name] = CartItem(product, quantity)

    def remove_item(self, product_name):
        """Remove a product from the cart."""
        if product_name in self.items:
            del self.items[product_name]

    def update_quantity(self, product_name, quantity):
        """Update the quantity of a specific item in the cart."""
        if product_name in self.items and quantity > 0:
            self.items[product_name].quantity = quantity
        elif quantity <= 0:
            self.remove_item(product_name)

    def calculate_total(self, is_member=False):
        """Calculate the total price of all items in the cart."""
        total = 0
        for item in self.items.values():
            total += item.get_total_price(is_member)
        return total

    def empty_cart(self):
        """Remove all items from the cart."""
        self.items.clear()
