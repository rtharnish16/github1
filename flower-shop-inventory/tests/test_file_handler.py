from src.flower_shop.file_handler import (
    load_addons,
    load_orders,
    load_products,
    save_addons,
    save_orders,
    save_products,
)
from src.flower_shop.models import Addon, Order, Product


def test_products_round_trip(tmp_path):
    path = tmp_path / "products.txt"
    products = [
        Product("R001", "Angel Eyes", "Romantic", 85.0, "Available"),
        Product("B001", "Birthday Bliss", "Birthday", 60.0, "Unavailable"),
    ]
    save_products(products, path=path)

    loaded = load_products(path=path)
    assert len(loaded) == 2
    assert loaded[0].code == "R001"
    assert loaded[0].price == 85.0


def test_load_products_skips_malformed_lines(tmp_path):
    path = tmp_path / "products.txt"
    path.write_text("R001,Angel Eyes,Romantic,notanumber,Available\nB001,Birthday Bliss,Birthday,60.00,Available\n")

    loaded = load_products(path=path)
    assert len(loaded) == 1
    assert loaded[0].code == "B001"


def test_load_products_missing_file_returns_empty_list(tmp_path):
    assert load_products(path=tmp_path / "does_not_exist.txt") == []


def test_addons_round_trip(tmp_path):
    path = tmp_path / "addons.txt"
    addons = [Addon("ADD001", "Chocolates", 8.0, "Available")]
    save_addons(addons, path=path)

    loaded = load_addons(path=path)
    assert len(loaded) == 1
    assert loaded[0].name == "Chocolates"


def test_orders_round_trip_preserves_commas_in_free_text(tmp_path):
    path = tmp_path / "orders.txt"
    orders = [
        Order(
            order_id="BBO-25-0001",
            product_code="R001",
            product_name="Angel Eyes",
            addon_code="ADD001",
            addon_name="Chocolates",
            customer_name="Tony Lin",
            recipient_name="Linda Foo",
            message="Congrats, well done!",
            delivery_type="Delivery",
            address="123 ABC Street",
            delivery_date="28-08-2025",
            same_day="N",
            delivery_fee=35.0,
            total=128.0,
            status="Open",
        )
    ]
    save_orders(orders, path=path)

    loaded = load_orders(path=path)
    assert len(loaded) == 1
    assert loaded[0].order_id == "BBO-25-0001"
    assert loaded[0].total == 128.0
    # The comma in the message was escaped, not silently dropped.
    assert ";" in loaded[0].message
