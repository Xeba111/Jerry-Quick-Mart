from product import Product

"""
    This class defines the inventory of the Store, given in a .txt file
        It has:
        - Name
        - Quantity
        - Regular Price
        - Member Price
        - Tax Status
"""


class Inventory:
    def __init__(self, inventory_file):
        self.products = {}  # Dictionary to store products, keyed by product name
        self.load_inventory(inventory_file)

    # ***** FUNCTIONS ***** #
    def load_inventory(self, inventory_file):
        """Load products from a given inventory file."""
        with open(inventory_file, 'r') as file:
            for line in file:
                parts = line.strip().split(':')
                name = parts[0].strip()
                details = parts[1].split(',')
                quantity = int(details[0].strip())
                regular_price = float(details[1].strip().replace('$', ''))
                member_price = float(details[2].strip().replace('$', ''))
                tax_status = details[3].strip()

                self.products[name] = Product(
                    name, quantity, regular_price, member_price, tax_status)

    def update_quantity(self, product_name, quantity):
        """Update the quantity of a product."""
        if product_name in self.products:
            self.products[product_name].quantity = quantity
        else:
            print(f"Product {product_name} not found.")

    def save_inventory(self, inventory_file):
        """Save the current state of the inventory back to the inventory file."""
        with open(inventory_file, 'w') as file:
            for product in self.products.values():
                line = f"{product.name}: {product.quantity}, ${product.regular_price:.2f}, ${
                    product.member_price:.2f}, {product.tax_status}\n"
                file.write(line)
