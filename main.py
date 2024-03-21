from PyQt6.QtWidgets import QApplication
from inventory import Inventory
from quick_mart_gui import QuickMartApp

if __name__ == "__main__":
    import sys

    inventory = Inventory('./Inventory/inventory.txt')
    app = QApplication(sys.argv)

    # Sheet styling to ensure uniform font style
    app.setStyleSheet("""
    QLabel, QRadioButton, QDateEdit, QLineEdit{
        font-size: 14px; /* Adjust size as needed */
        font-weight: normal; 
    }
    QTableWidget {
        font-size: 15px; /* Custom size for table content */
        font-weight: normal; /* Standard font weight for table */
    }
    QPushButton {
        font-size: 14px; /* Custom size for table content */
        font-weight: normal; /* Standard font weight for table */
    }
    QHeaderView::section {
        background-color: #A0A0A0; /* Custom background for table headers */
        font-size: 15px; /* Larger text for table headers */
        font-weight: normal; /* Bold text for table headers */
    }
    """)

    window = QuickMartApp(inventory)
    window.show()
    sys.exit(app.exec())
