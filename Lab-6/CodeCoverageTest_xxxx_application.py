
import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


def test_invalid_orders_input():
    with pytest.raises(ValueError):
        process_order_batch("not-a-list", 0.1)


def test_unpaid_order_is_skipped():
    result = process_order_batch(
        [{"paid": False}], 0.1
    )
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_small_medium_and_large_orders():
    orders = [
        {"paid": True, "size": "small"},
        {"paid": True, "size": "medium"},
        {"paid": True, "size": "large", "is_member": True},
    ]
    result = process_order_batch(orders, 0.1)
    assert result == {"total": 14.19, "status": "COMPLETED"}


def test_unknown_size_is_rejected():
    result = process_order_batch(
        [{"paid": True, "size": "extra-large"}], 0.1
    )
    assert result == {"total": 0.0, "status": "NO_SALE"}

def test_negative_customization_cost():
    orders = [{
        "paid": True,
        "size": "medium",
        "customizations": [
            {"type": "standard", "cost": -2.0},
            {"type": "standard", "cost": 0.5},
        ],
    }]
    result = process_order_batch(orders, 0.1)
    assert result == {"total": 5.5, "status": "COMPLETED"}


def test_strict_allergy_alert():
    orders = [{
        "paid": True,
        "size": "medium",
        "strict_allergy": True,
        "customizations": [
            {"type": "allergen_alert", "cost": 0.0}
        ],
    }]
    result = process_order_batch(orders, 0.1)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_syrup_cost_is_capped():
    orders = [{
        "paid": True,
        "size": "medium",
        "customizations": [
            {"type": "syrup", "cost": 2.0}
        ],
    }]
    result = process_order_batch(orders, 0.1)
    assert result == {"total": 6.6, "status": "COMPLETED"}


def test_more_than_four_rejections():
    orders = [
        {"paid": True, "size": "unknown"}
        for _ in range(5)
    ]
    result = process_order_batch(orders, 0.1)
    assert result == {"total": 0.0, "status": "AUDIT_REJECTED"}


def test_empty_temperature_data():
    assert check_espresso_machine([]) == "NO_DATA"


def test_espresso_machine_optimal():
    assert check_espresso_machine(
        [[97.0, 96.0, 97.0]]
    ) == "OPTIMAL"

def test_espresso_machine_shutdown():
    assert check_espresso_machine(
        [[97.0, 98.0]]
    ) == "SHUTDOWN"
