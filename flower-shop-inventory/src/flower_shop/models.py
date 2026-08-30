"""Data models used across the Beautiful Blooms Inventory & Sales system.

Each model is a small, self-contained record. Keeping them dependency-free
makes them trivial to unit test and to serialize to/from the plain-text
data files used for persistence (see ``file_handler.py``).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Product:
    """A single flower/bouquet ("bloom") offered by the shop."""

    code: str
    name: str
    category: str
    price: float
    status: str = "Available"

    @property
    def is_available(self) -> bool:
        return self.status.strip().lower() == "available"

    def to_row(self) -> str:
        """Serialize to a comma-separated line for ``products.txt``."""
        return f"{self.code},{self.name},{self.category},{self.price:.2f},{self.status}"


@dataclass
class Addon:
    """An optional extra (chocolates, teddy bear, card, ...) added to an order."""

    code: str
    name: str
    price: float
    status: str = "Available"

    @property
    def is_available(self) -> bool:
        return self.status.strip().lower() == "available"

    def to_row(self) -> str:
        """Serialize to a comma-separated line for ``addons.txt``."""
        return f"{self.code},{self.name},{self.price:.2f},{self.status}"


@dataclass
class Order:
    """A customer order, linking a product with an optional add-on."""

    order_id: str
    product_code: str
    product_name: str
    addon_code: str
    addon_name: str
    customer_name: str
    recipient_name: str
    message: str
    delivery_type: str  # "Pickup" or "Delivery"
    address: str
    delivery_date: str
    same_day: str  # "Y" or "N"
    delivery_fee: float
    total: float
    status: str = "Open"

    def to_row(self) -> str:
        """Serialize to a comma-separated line for ``orders.txt``.

        Free-text fields (customer name, recipient, message, address) are
        semicolon-escaped so a comma the user typed can't be mistaken for a
        field separator when the line is parsed back in.
        """
        fields = [
            self.order_id,
            self.product_code,
            self.product_name,
            self.addon_code,
            self.addon_name,
            _escape(self.customer_name),
            _escape(self.recipient_name),
            _escape(self.message),
            self.delivery_type,
            _escape(self.address),
            self.delivery_date,
            self.same_day,
            f"{self.delivery_fee:.2f}",
            f"{self.total:.2f}",
            self.status,
        ]
        return ",".join(fields)


def _escape(value: str) -> str:
    """Replace commas in free-text fields so the CSV-style row stays valid."""
    return value.replace(",", ";") if value else ""
