from datetime import date

from src.flower_shop.validators import (
    generate_order_id,
    generate_unique_code,
    is_valid_name,
    is_weekend,
    parse_delivery_date,
)


def test_generate_unique_code_first_of_prefix():
    assert generate_unique_code([], "R") == "R001"


def test_generate_unique_code_increments_highest():
    assert generate_unique_code(["R001", "R002", "B001"], "R") == "R003"


def test_generate_unique_code_ignores_other_prefixes():
    assert generate_unique_code(["ADD001", "ADD002"], "R") == "R001"


def test_generate_order_id_first_of_year():
    order_id = generate_order_id([], today=date(2025, 8, 28))
    assert order_id == "BBO-25-0001"


def test_generate_order_id_increments():
    existing = ["BBO-25-0001", "BBO-25-0002"]
    order_id = generate_order_id(existing, today=date(2025, 8, 28))
    assert order_id == "BBO-25-0003"


def test_generate_order_id_resets_for_new_year():
    existing = ["BBO-25-0009"]
    order_id = generate_order_id(existing, today=date(2026, 1, 2))
    assert order_id == "BBO-26-0001"


def test_parse_delivery_date_accepts_both_formats():
    assert parse_delivery_date("28-08-2025") == date(2025, 8, 28)
    assert parse_delivery_date("2025-08-28") == date(2025, 8, 28)


def test_parse_delivery_date_rejects_garbage():
    assert parse_delivery_date("not-a-date") is None


def test_is_weekend():
    assert is_weekend(date(2025, 8, 30)) is True  # Saturday
    assert is_weekend(date(2025, 8, 28)) is False  # Thursday


def test_is_valid_name():
    assert is_valid_name("Tony Lin") is True
    assert is_valid_name("   ") is False
    assert is_valid_name("") is False
