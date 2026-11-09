
import pytest
from coffee_shop_order import process_order_batch, check_espresso_machine


def test_invalid_orders_type():
    with pytest.raises(ValueError):
        process_order_batch(None, 0.1)


def test_negative_tax_rate():
    with pytest.raises(ValueError):
        process_order_batch([], -0.1)


def test_empty_orders_list():
    assert process_order_batch([], 0.1) == {
        "total": 0.0, "status": "NO_SALE"
    }


def test_unpaid_order():
    result = process_order_batch([{"paid": False}], 0.1)
    assert result["status"] == "NO_SALE"


def test_all_coffee_sizes():
    orders = [
        {"paid": True, "size": "small"},
        {"paid": True, "size": "medium"},
        {"paid": True, "size": "large", "is_member": True},
    ]

    result = process_order_batch(orders, 0.1)
    assert result == {"total": 14.19, "status": "COMPLETED"}


def test_unknown_coffee_size():
    result = process_order_batch(
        [{"paid": True, "size": "extra-large"}], 0.1
    )
    assert result["status"] == "NO_SALE"


def test_default_order_values():
    result = process_order_batch([{"paid": True}], 0.1)
    assert result == {"total": 4.95, "status": "COMPLETED"}


def test_empty_customizations():
    order = [{"paid": True, "size": "medium", "customizations": []}]
    result = process_order_batch(order, 0.1)
    assert result["total"] == 4.95


def test_negative_customization_cost():
    order = [{
        "paid": True,
        "size": "medium",
        "customizations": [
            {"type": "standard", "cost": -2.0},
            {"type": "standard", "cost": 0.5},
        ],
    }]
    result = process_order_batch(order, 0.1)
    assert result["total"] == 5.5


def test_non_strict_allergy_alert():
    order = [{
        "paid": True,
        "size": "medium",
        "strict_allergy": False,
        "customizations": [
            {"type": "allergen_alert", "cost": 0.0}
        ],
    }]
    result = process_order_batch(order, 0.1)
    assert result == {"total": 4.95, "status": "COMPLETED"}


def test_strict_allergy_alert():
    order = [{
        "paid": True,
        "size": "medium",
        "strict_allergy": True,
        "customizations": [
            {"type": "allergen_alert", "cost": 0.0}
        ],
    }]
    result = process_order_batch(order, 0.1)
    assert result == {"total": 0.0, "status": "NO_SALE"}


def test_syrup_cost_within_limit():
    order = [{
        "paid": True,
        "size": "medium",
        "customizations": [{"type": "syrup", "cost": 1.0}],
    }]
    result = process_order_batch(order, 0.1)
    assert result["total"] == 6.05


def test_syrup_cost_above_limit():
    order = [{
        "paid": True,
        "size": "medium",
        "customizations": [{"type": "syrup", "cost": 2.0}],
    }]
    result = process_order_batch(order, 0.1)
    assert result["total"] == 6.6


def test_standard_customization():
    order = [{
        "paid": True,
        "size": "medium",
        "customizations": [{"type": "standard", "cost": 0.5}],
    }]
    result = process_order_batch(order, 0.1)
    assert result["total"] == 5.5


def test_more_than_four_rejected_items():
    orders = [
        {"paid": True, "size": "unknown"}
        for _ in range(5)
    ]
    result = process_order_batch(orders, 0.1)
    assert result["status"] == "AUDIT_REJECTED"


def test_fewer_than_five_rejections():
    orders = [
        {"paid": True, "size": "unknown"},
        {"paid": True, "size": "medium"},
    ]
    result = process_order_batch(orders, 0.1)
    assert result == {"total": 4.95, "status": "COMPLETED"}


def test_no_temperature_data():
    assert check_espresso_machine([]) == "NO_DATA"


def test_empty_temperature_cycle():
    assert check_espresso_machine([[]]) == "OPTIMAL"


def test_temperature_at_safe_limit():
    assert check_espresso_machine([[96.0]]) == "OPTIMAL"


def test_overheating_without_consecutive_streak():
    assert check_espresso_machine([[97.0, 96.0, 97.0]]) == "OPTIMAL"


def test_streak_resets_between_cycles():
    assert check_espresso_machine([[97.0], [97.0]]) == "OPTIMAL"


def test_two_consecutive_overheating_readings():
    assert check_espresso_machine([[97.0, 98.0]]) == "SHUTDOWN"
