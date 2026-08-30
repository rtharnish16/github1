"""Inventory Management: managing blooms (products) and add-ons."""

from __future__ import annotations

from .file_handler import save_addons, save_products
from .models import Addon, Product
from .validators import generate_unique_code, read_float

CATEGORIES = {
    "1": "Romantic",
    "2": "Birthday",
    "3": "Grand Opening",
    "4": "Condolence",
    "5": "Anniversary",
}


def find_product_by_code(products: list[Product], code: str) -> Product | None:
    code = code.strip().upper()
    for product in products:
        if product.code.upper() == code:
            return product
    return None


def find_addon_by_code(addons: list[Addon], code: str) -> Addon | None:
    code = code.strip().upper()
    for addon in addons:
        if addon.code.upper() == code:
            return addon
    return None


def inventory_menu(products: list[Product], addons: list[Addon]) -> None:
    """Top-level Inventory Management menu (Main Menu option 1)."""
    while True:
        print("\n==== Inventory Management ====")
        print("1. View/Update Blooms")
        print("2. Add New Bloom")
        print("3. View/Update Add-ons")
        print("4. Add New Add-on")
        print("5. Back to Main Menu")
        choice = input("Enter option: ").strip()

        if choice == "1":
            view_update_blooms(products)
        elif choice == "2":
            add_new_bloom(products)
        elif choice == "3":
            view_update_addons(addons)
        elif choice == "4":
            add_new_addon(addons)
        elif choice == "5":
            return
        else:
            print("Invalid option. Try again.")


def _print_products(products: list[Product]) -> None:
    if not products:
        print("(No blooms in inventory.)")
        return
    print(f"{'Code':<8}{'Name':<25}{'Category':<15}{'Price':<9}{'Status':<12}")
    for p in products:
        print(f"{p.code:<8}{p.name:<25}{p.category:<15}${p.price:<8.2f}{p.status:<12}")


def view_update_blooms(products: list[Product]) -> None:
    _print_products(products)
    code = input("\nEnter item code to update (or 0 to go back): ").strip()
    if code == "0":
        return

    product = find_product_by_code(products, code)
    if not product:
        print("Invalid item code.")
        return

    print(f"Updating {product.name} ({product.code})")
    new_price = input(f"New price [{product.price:.2f}] (blank to keep): ").strip()
    if new_price:
        try:
            product.price = float(new_price)
        except ValueError:
            print("Invalid price. Keeping previous value.")

    new_status = input(
        f"New status [{product.status}] (Available/Unavailable, blank to keep): "
    ).strip()
    if new_status:
        if new_status.title() in ("Available", "Unavailable"):
            product.status = new_status.title()
        else:
            print("Invalid status. Keeping previous value.")

    save_products(products)
    print("Bloom updated successfully.")


def add_new_bloom(products: list[Product]) -> None:
    print("\nSelect a category:")
    for key, label in CATEGORIES.items():
        print(f"{key}. {label}")
    cat_choice = input("Enter option: ").strip()
    category = CATEGORIES.get(cat_choice)
    if not category:
        print("Invalid category. Bloom not added.")
        return

    name = input("Enter bloom name: ").strip()
    if not name:
        print("Name cannot be empty. Bloom not added.")
        return

    price = read_float("Enter price: ")
    if price is None or price < 0:
        print("Invalid price. Bloom not added.")
        return

    code = generate_unique_code([p.code for p in products], prefix=category[0].upper())
    products.append(Product(code, name, category, price, "Available"))
    save_products(products)
    print(f"Bloom added successfully (Code: {code})")


def _print_addons(addons: list[Addon]) -> None:
    if not addons:
        print("(No add-ons in inventory.)")
        return
    print(f"{'Code':<10}{'Name':<25}{'Price':<9}{'Status':<12}")
    for a in addons:
        print(f"{a.code:<10}{a.name:<25}${a.price:<8.2f}{a.status:<12}")


def view_update_addons(addons: list[Addon]) -> None:
    _print_addons(addons)
    code = input("\nEnter add-on code to update (or 0 to go back): ").strip()
    if code == "0":
        return

    addon = find_addon_by_code(addons, code)
    if not addon:
        print("Invalid add-on code.")
        return

    print(f"Updating {addon.name} ({addon.code})")
    new_price = input(f"New price [{addon.price:.2f}] (blank to keep): ").strip()
    if new_price:
        try:
            addon.price = float(new_price)
        except ValueError:
            print("Invalid price. Keeping previous value.")

    new_status = input(
        f"New status [{addon.status}] (Available/Unavailable, blank to keep): "
    ).strip()
    if new_status:
        if new_status.title() in ("Available", "Unavailable"):
            addon.status = new_status.title()
        else:
            print("Invalid status. Keeping previous value.")

    save_addons(addons)
    print("Add-on updated successfully.")


def add_new_addon(addons: list[Addon]) -> None:
    name = input("Enter add-on name: ").strip()
    if not name:
        print("Name cannot be empty. Add-on not added.")
        return

    price = read_float("Enter price: ")
    if price is None or price < 0:
        print("Invalid price. Add-on not added.")
        return

    code = generate_unique_code([a.code for a in addons], prefix="ADD")
    addons.append(Addon(code, name, price, "Available"))
    save_addons(addons)
    print(f"Add-on added successfully (Code: {code})")
