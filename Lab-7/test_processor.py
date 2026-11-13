from hypothesis import given, strategies as st
from processor import lookup_drink_code, calculate_average_shot_cost, parse_order_modifiers

@given(st.text() | st.none())
def test_lookup_drink_code_no_crash(s):
    try:
        lookup_drink_code(s)
    except Exception as e:
        assert False, f"lookup_drink_code crashed with: {e}"

@given(st.text() | st.none())
def test_calculate_average_shot_cost_safe(s):
    try:
        calculate_average_shot_cost(s)
    except Exception as e:
        assert False, f"calculate_average_shot_cost crashed with: {e}"

@given(st.text() | st.none())
def test_parse_order_modifiers_safe(s):
    try:
        parse_order_modifiers(s)
    except Exception as e:
        assert False, f"parse_order_modifiers crashed with: {e}"

