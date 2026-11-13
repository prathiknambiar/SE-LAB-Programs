
def lookup_drink_code(code_string):
    if not isinstance(code_string, str):
        return None

    code_prefix = code_string.strip().upper()[:3]

    menu_prices = {
        "LAT": 4.50,
        "CAP": 4.00,
        "ESP": 3.00,
        "AME": 3.50,
        "MOC": 5.00
    }

    return menu_prices.get(code_prefix)


def calculate_average_shot_cost(pricing_csv):
    if not isinstance(pricing_csv, str) or not pricing_csv.strip():
        return 0.0

    try:
        prices = [float(p.strip()) for p in pricing_csv.split(',')]

        if not prices:
            return 0.0

        if any(not (price >= 0 and price < float('inf')) for price in prices):
            return 0.0

        return sum(prices) / len(prices)

    except (ValueError, TypeError):
        return 0.0


def parse_order_modifiers(order_spec):
    if not isinstance(order_spec, str) or not order_spec.strip():
        return {}

    modifier_dict = {}

    for item in order_spec.split(';'):
        if ':' not in item:
            continue

        key, value = item.split(':', 1)

        key = key.strip()
        value = value.strip()

        if key:
            modifier_dict[key] = value

    return modifier_dict


def main():
    print("==== Running lookup_drink_code ====")
    drink_input = input("Enter drink code prefix (e.g. LAT, CAP, ESP): ")
    price = lookup_drink_code(drink_input)
    print("Base Price: $", price)

    print("\n==== Running calculate_average_shot_cost ====")
    shots_input = input("Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): ")
    avg_price = calculate_average_shot_cost(shots_input)
    print("Average Shot Price: $", avg_price)

    print("\n==== Running parse_order_modifiers ====")
    spec_input = input("Enter modifiers (e.g. milk:oat;syrup:vanilla): ")
    mods = parse_order_modifiers(spec_input)
    print("Parsed Modifiers:", mods)


if __name__ == "__main__":
    main()

