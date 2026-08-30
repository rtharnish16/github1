"""Entry point for the Beautiful Blooms Florist Management System.

Run with:  python -m src.flower_shop.main   (from the project root)
"""

from __future__ import annotations

from .file_handler import load_addons, load_orders, load_products
from .inventory import inventory_menu
from .sales import sales_menu


def main() -> None:
    products = load_products()
    addons = load_addons()
    orders = load_orders()

    exit_flag = False
    while not exit_flag:
        print("\n@@@@ Beautiful Blooms @@@@")
        print("1. Inventory Management")
        print("2. Sales Management")
        print("3. Exit")
        option = input("Enter option: ").strip()

        if option == "1":
            inventory_menu(products, addons)
        elif option == "2":
            sales_menu(products, addons, orders)
        elif option == "3":
            exit_flag = True
        else:
            print("Invalid option. Try again.")

    print("Exiting Beautiful Blooms system. Goodbye!")


if __name__ == "__main__":
    main()
