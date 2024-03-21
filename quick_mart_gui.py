from inventory import Inventory
from product import Product
from cart import Cart
from cart_item import CartItem
from transaction import Transaction
from PyQt6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QRadioButton, QHBoxLayout, QLabel, QAbstractItemView, QMessageBox, QLineEdit, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon, QDoubleValidator
from PyQt6.QtCore import QDate
from datetime import date, datetime


"""
    This class is the Graphic User Interface of the program. It ensures all the functionality of the GUI thanks to the Transacion class.
    Its attributes are:
        - Invetory file, relative path of the Inventory to save the information according to the transaction
        - Inventory, real inventory 
        - Member Status, verified by the button in the GUI
        - Transaction ID
        - Cash, the ammount of currency the user has used to pay.  
"""


class QuickMartApp(QMainWindow):
    def __init__(self, inventory):
        super().__init__()
        self.inventory_file = './Inventory/inventory.txt'
        self.inventory = inventory
        self.cart = Cart()
        self.is_member = False
        self.transaction_id_counter = 0
        self.cash = 0.0

        # Window definition
        self.setWindowTitle("Jerry's Quick Mart")
        self.setGeometry(100, 100, 800, 600)

        # Set the window Icon
        self.setWindowIcon(QIcon('./Resources/icon.jpg'))

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Set the base layout
        self.layout = QVBoxLayout()

        # Date Field
        self.date_layout = QHBoxLayout()
        today = date.today()
        self.date_layout.addWidget(QLabel("Current Date:"))
        self.date_label = QLabel(today.strftime('%d-%m-%Y'))
        self.date_label.setStyleSheet(
            "font-size: 16px; qproperty-alignment: 'AlignCenter'; font-weight: bold")
        self.date_layout.addWidget(self.date_label)
        self.layout.addLayout(self.date_layout)

        # Customer Type Selection
        self.customer_type_layout = QHBoxLayout()
        self.regular_radio = QRadioButton("Regular Member")
        self.member_radio = QRadioButton("Rewards Member")
        self.customer_type_layout.addWidget(QLabel("Customer Type:"))
        self.customer_type_layout.addWidget(self.regular_radio)
        self.customer_type_layout.addWidget(self.member_radio)
        self.regular_radio.setChecked(True)  # Default selection
        self.regular_radio.toggled.connect(self.update_customer_type)
        self.member_radio.toggled.connect(self.update_customer_type)
        self.layout.addLayout(self.customer_type_layout)

        # Inventory Table
        self.label_inventory = QLabel("Inventory Table")
        self.label_inventory.setStyleSheet(
            "font-size: 20px; qproperty-alignment: 'AlignCenter'; font-weight: bold")
        self.layout.addWidget(self.label_inventory)

        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(5)
        self.inventory_table.setHorizontalHeaderLabels(
            ["Name", "Quantity", "Regular Price", "Member Price", "Tax Status"])

        self.inventory_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self.inventory_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection)

        self.inventory_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers)
        self.layout.addWidget(self.inventory_table)

        # Buttons for cart management
        self.buttons_layout = QHBoxLayout()
        self.add_item_button = QPushButton("Add Item to Cart")
        self.remove_item_button = QPushButton("Remove Item from Cart")
        self.empty_cart_button = QPushButton("Empty Cart")

        self.add_item_button.clicked.connect(self.add_item)
        self.remove_item_button.clicked.connect(self.remove_item)
        self.empty_cart_button.clicked.connect(self.empty_cart)

        self.buttons_layout.addWidget(self.add_item_button)
        self.buttons_layout.addWidget(self.remove_item_button)
        self.buttons_layout.addWidget(self.empty_cart_button)
        self.layout.addLayout(self.buttons_layout)

        # Spacing
        spacer = QSpacerItem(
            10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addItem(spacer)

        # Cart Table
        self.label_cart = QLabel("Cart Table")
        self.label_cart.setStyleSheet(
            "font-size: 20px; qproperty-alignment: 'AlignCenter'; font-weight: bold")
        self.layout.addWidget(self.label_cart)

        self.cart_table = QTableWidget()
        self.cart_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers)

        # Name, Quantity, Unit Price,Total Price
        self.cart_table.setColumnCount(4)
        self.cart_table.setHorizontalHeaderLabels(
            ["Name", "Quantity", "Unit Price", "Total Price"])
        self.cart_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows)
        self.cart_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection)
        self.layout.addWidget(self.cart_table)
        self.cart_table.resizeColumnsToContents()

        # Buttons for cash input
        self.buttons_layout_cash = QHBoxLayout()
        validator = QDoubleValidator(0.0, 100.0, 2)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)

        # Create text field
        self.cash_input = QLineEdit(self)
        self.cash_input.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.cash_input.setMaximumWidth(200)  # Set the maximum width
        self.cash_input.setValidator(validator)
        self.cash_input.setPlaceholderText("Enter a value up to $1000")
        self.confirm_money = QPushButton("Confirm money")
        self.reset_money = QPushButton("Reset money")

        self.confirm_money.clicked.connect(self.confirm_value)
        self.reset_money.clicked.connect(self.reset_value)

        self.buttons_layout_cash.addWidget(self.cash_input)
        self.buttons_layout_cash.addWidget(self.confirm_money)
        self.buttons_layout_cash.addWidget(self.reset_money)
        self.layout.addLayout(self.buttons_layout_cash)

        # Spacing
        spacer = QSpacerItem(
            10, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.layout.addItem(spacer)

        # Buttons for generaring receipt and finalizing
        self.buttons_layout2 = QHBoxLayout()
        self.finalize_transaction_button = QPushButton("Finalize Transaction")
        self.preview_receipt_button = QPushButton("Preview Receipt")
        self.finalize_transaction_button.clicked.connect(
            self.confirm_action)
        self.preview_receipt_button.clicked.connect(self.preview_receipt)

        self.buttons_layout2.addWidget(self.finalize_transaction_button)
        self.buttons_layout2.addWidget(self.preview_receipt_button)
        self.layout.addLayout(self.buttons_layout2)

        self.main_widget.setLayout(self.layout)

        self.populate_inventory_table()

    # ***** FUNCTIONS ***** #

    def update_customer_type(self):
        """Check RadioButton to update user type"""
        self.is_member = self.member_radio.isChecked()
        self.populate_cart_table()  # Update cart prices based on customer type

    def populate_inventory_table(self):
        """Populate the inventory table given the Inventory object"""
        self.inventory_table.setRowCount(len(self.inventory.products))
        for i, (name, product) in enumerate(self.inventory.products.items()):
            self.inventory_table.setItem(i, 0, QTableWidgetItem(product.name))
            self.inventory_table.setItem(
                i, 1, QTableWidgetItem(str(product.quantity)))
            self.inventory_table.setItem(
                i, 2, QTableWidgetItem(f"${product.regular_price}"))
            self.inventory_table.setItem(
                i, 3, QTableWidgetItem(f"${product.member_price}"))
            self.inventory_table.setItem(
                i, 4, QTableWidgetItem(product.tax_status))

    def populate_cart_table(self):
        """Populate the cart table given the Cart object"""
        self.cart_table.setRowCount(len(self.cart.items))
        for i, (product_name, cart_item) in enumerate(self.cart.items.items()):
            self.cart_table.setItem(i, 0, QTableWidgetItem(product_name))
            self.cart_table.setItem(
                i, 1, QTableWidgetItem(str(cart_item.quantity)))
            self.cart_table.setItem(i, 2, QTableWidgetItem(
                f"${cart_item.get_unit_price(self.is_member)}"))
            self.cart_table.setItem(i, 3, QTableWidgetItem(
                f"${cart_item.get_total_price(self.is_member):.2f}"))

    def add_item(self):
        """Add item to the cart. This only adds one item"""
        selected_row = self.inventory_table.currentRow()
        if selected_row != -1:
            product_name = self.inventory_table.item(selected_row, 0).text()
            product = self.inventory.products.get(product_name)
            if product and self.inventory.products[product_name].quantity >= 1:
                # Check if the item is already in the cart to update quantity
                if product_name in self.cart.items:
                    if self.inventory.products[product_name].quantity > self.cart.items[product_name].quantity:
                        self.cart.items[product_name].quantity += 1
                    else:
                        self.cart.items[product_name].quantity
                else:
                    self.cart.add_item(product, 1)
                self.populate_cart_table()

    def remove_item(self):
        """Remove item to the cart. This only removes one item"""
        selected_row = self.cart_table.currentRow()
        if selected_row != -1:
            product_name = self.cart_table.item(selected_row, 0).text()
            if product_name in self.cart.items:
                if self.cart.items[product_name].quantity == 1:
                    del self.cart.items[product_name]
                else:
                    self.cart.items[product_name].quantity -= 1
                self.populate_cart_table()

    def empty_cart(self):
        """Remove all items from the cart"""
        self.cart.empty_cart()
        self.populate_cart_table()

    def finalize_transaction(self):
        """Finalizes the transaction using the Transaction class"""

        self.transaction_id_counter += 1
        transaction_id = f"{self.transaction_id_counter:04d}"

        transaction = Transaction(
            self.inventory, self.cart, self.is_member, transaction_id)
        receipt = transaction.finalize(self.cash)
        QMessageBox.information(
            self, "Transaction Successful", "The transaction has been aproved!")
        self.inventory.save_inventory(self.inventory_file)
        self.cart.empty_cart()
        self.reset_value
        self.populate_cart_table()
        self.populate_inventory_table()

    def preview_receipt(self):
        """Previews the receipt using the Transaction class"""
        if not self.cart.items:
            return QMessageBox.information(self, "Transaction Failed", "The transaction has failed, the cart is currently empty")

        transaction_id = f"Preview_{self.transaction_id_counter + 1:04d}"

        transaction = Transaction(
            self.inventory, self.cart, self.is_member, transaction_id)
        receipt_preview = transaction.generate_receipt(self.cash)

        msgBox = QMessageBox()
        msgBox.setWindowTitle("Receipt Preview")
        msgBox.setText("Receipt Preview:\n" + receipt_preview)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()

    def confirm_value(self):
        """Confirms cash value entered in the text field"""
        if self.cash_input.text() != "" and float(self.cash_input.text()) != 0.0:
            self.cash = float(self.cash_input.text())
        else:
            return QMessageBox.information(self, "Action Failed", "Please enter a valid value")

    def reset_value(self):
        """Resets cash value entered in the text field"""
        self.cash = 0.0
        self.cash_input.setText("0")

    def confirm_action(self):
        """Confirms the finalization of the transaction"""

        if not self.cart.items:
            return QMessageBox.information(self, "Transaction Failed", "The transaction has failed, the cart is currently empty")

        if self.cash == 0.0:
            return QMessageBox.information(self, "Transaction Failed", "The user has not paid yet!")

        reply = QMessageBox.question(self, 'Confirm Action',
                                     'Are you sure you want to finish the transaction?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.finalize_transaction()
        else:
            return QMessageBox.information(self, "Action Cancelled", "You have cancelled the transaction")
