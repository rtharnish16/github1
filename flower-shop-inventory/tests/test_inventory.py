from src.flower_shop.inventory import find_addon_by_code, find_product_by_code
from src.flower_shop.models import Addon, Product


def sample_products():
    return [
        Product("R001", "Angel Eyes", "Romantic", 85.0, "Available"),
        Product("B001", "Birthday Bliss", "Birthday", 60.0, "Unavailable"),
    ]


def sample_addons():
    return [Addon("ADD001", "Chocolates", 8.0, "Available")]


def test_find_product_by_code_found():
    product = find_product_by_code(sample_products(), "R001")
    assert product is not None
    assert product.name == "Angel Eyes"


def test_find_product_by_code_case_insensitive():
    product = find_product_by_code(sample_products(), "r001")
    assert product is not None


def test_find_product_by_code_not_found():
    assert find_product_by_code(sample_products(), "X999") is None


def test_find_addon_by_code_found():
    addon = find_addon_by_code(sample_addons(), "ADD001")
    assert addon is not None
    assert addon.name == "Chocolates"


def test_product_is_available():
    products = sample_products()
    assert products[0].is_available is True
    assert products[1].is_available is False


def test_product_to_row_round_trip():
    product = Product("R001", "Angel Eyes", "Romantic", 85.0, "Available")
    row = product.to_row()
    assert row == "R001,Angel Eyes,Romantic,85.00,Available"
