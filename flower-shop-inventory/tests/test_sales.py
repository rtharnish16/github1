from datetime import date

from src.flower_shop.sales import (
    DELIVERY_FEE,
    PICKUP_FEE,
    SAME_DAY_SURCHARGE,
    WEEKEND_SURCHARGE,
    calculate_delivery_fee,
)


def test_pickup_is_free():
    assert calculate_delivery_fee("Pickup", "N", None) == PICKUP_FEE


def test_weekday_delivery_flat_fee():
    weekday = date(2025, 8, 28)  # Thursday
    assert calculate_delivery_fee("Delivery", "N", weekday) == DELIVERY_FEE


def test_weekend_delivery_adds_surcharge():
    saturday = date(2025, 8, 30)
    assert calculate_delivery_fee("Delivery", "N", saturday) == DELIVERY_FEE + WEEKEND_SURCHARGE


def test_same_day_delivery_adds_surcharge():
    weekday = date(2025, 8, 28)
    assert calculate_delivery_fee("Delivery", "Y", weekday) == DELIVERY_FEE + SAME_DAY_SURCHARGE


def test_same_day_weekend_delivery_stacks_both_surcharges():
    saturday = date(2025, 8, 30)
    expected = DELIVERY_FEE + SAME_DAY_SURCHARGE + WEEKEND_SURCHARGE
    assert calculate_delivery_fee("Delivery", "Y", saturday) == expected
