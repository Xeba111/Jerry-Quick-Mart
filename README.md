# Jerry-Quick-Mart

## Instructions
- Clone the repository to any directory.
- Install requirements by using any Python 3.12 environment and running the command.
  - pip install -r requirements.txt
- Run the program with the same environment that has the necessary libraries installed.

## Explanation
This app uses PyQt6 to provide a easy to use GUI. It is a solution that uses OOP to facilitate the integration between GUI and logic. Due to OOP principles, information can be stored within the classes themselves, read through the provided 'inventory.txt' file in the Inventory folder.
This solution includes:
- Product class: This class defines the most basic of Objects in this project.
- Inventory: This class defines the inventory of the Store, given in a .txt file. The Inventory contains Products.
- CartItem: This class defines CartItem, a class that stores a Product and its quantity.
- Cart: This class defines the client's Cart object. The Cart contains CartItems.
- Transaction: This class defines the current transaction. This class allows everything related to the preview of the receipt and also the finalization of the current session.This class interacts with the GUI. A transaction includes the Cart object.

## Assumptions:
Some assumptions made by this solutions are:
- The user will use the correct decimal separator, the dot (.)
- The user won't close the application in a working day, otherwise the ID be restored back to 0001 and overwrite other transactions.
- The user won't modify the inventory.txt file while the application is running, otherwise the GUI will not read the new changes.
