"""Loading and saving Products, Add-ons and Orders to plain-text files.

The system deliberately avoids a database: three lightweight, human-readable
text files (``products.txt``, ``addons.txt``, ``orders.txt``) are enough for
a small shop, are easy to inspect/edit by hand, and keep the project focused
on core Python (file I/O, parsing, validation) rather than external
dependencies.
"""

from __future__ import annotations

from pathlib import Path

from .models import Addon, Order, Product

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
PRODUCTS_FILE = DATA_DIR / "products.txt"
ADDONS_FILE = DATA_DIR / "addons.txt"
ORDERS_FILE = DATA_DIR / "orders.txt"


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_products(path: Path = PRODUCTS_FILE) -> list[Product]:
    """Read ``products.txt`` into a list of :class:`Product` objects.

    Malformed lines (wrong column count, non-numeric price) are skipped
    rather than crashing the whole program, matching the "resilient to bad
    data" behaviour described for the original system.
    """
    products: list[Product] = []
    if not path.exists():
        return products

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) < 5:
                continue
            code, name, category, price, status = parts[:5]
            try:
                products.append(Product(code, name, category, float(price), status))
            except ValueError:
                continue
    return products


def load_addons(path: Path = ADDONS_FILE) -> list[Addon]:
    """Read ``addons.txt`` into a list of :class:`Addon` objects."""
    addons: list[Addon] = []
    if not path.exists():
        return addons

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) < 4:
                continue
            code, name, price, status = parts[:4]
            try:
                addons.append(Addon(code, name, float(price), status))
            except ValueError:
                continue
    return addons


def load_orders(path: Path = ORDERS_FILE) -> list[Order]:
    """Read ``orders.txt`` into a list of :class:`Order` objects."""
    orders: list[Order] = []
    if not path.exists():
        return orders

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            parts = [p.strip() for p in line.strip().split(",")]
            if len(parts) < 15:
                continue
            try:
                orders.append(
                    Order(
                        order_id=parts[0],
                        product_code=parts[1],
                        product_name=parts[2],
                        addon_code=parts[3],
                        addon_name=parts[4],
                        customer_name=parts[5],
                        recipient_name=parts[6],
                        message=parts[7],
                        delivery_type=parts[8],
                        address=parts[9],
                        delivery_date=parts[10],
                        same_day=parts[11],
                        delivery_fee=float(parts[12]),
                        total=float(parts[13]),
                        status=parts[14],
                    )
                )
            except ValueError:
                continue
    return orders


def save_products(products: list[Product], path: Path = PRODUCTS_FILE) -> None:
    _ensure_data_dir()
    with path.open("w", encoding="utf-8") as f:
        for product in products:
            f.write(product.to_row() + "\n")


def save_addons(addons: list[Addon], path: Path = ADDONS_FILE) -> None:
    _ensure_data_dir()
    with path.open("w", encoding="utf-8") as f:
        for addon in addons:
            f.write(addon.to_row() + "\n")


def save_orders(orders: list[Order], path: Path = ORDERS_FILE) -> None:
    _ensure_data_dir()
    with path.open("w", encoding="utf-8") as f:
        for order in orders:
            f.write(order.to_row() + "\n")
