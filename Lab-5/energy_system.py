"""Energy consumption tracker and tiered tariff calculator."""

import json
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
LOGGER = logging.getLogger(__name__)

SPIKE_LIMIT = 500.0
DATA_FILE = Path("meters.json")


class EnergySystem:
    """Manage meter readings and electricity tariff calculations."""

    def __init__(self) -> None:
        self.meters: dict[str, float] = {}
        self.tier_rates = [3.5, 5.0, 7.5]

    def record_reading(self, meter_id: str, units: float) -> None:
        """Add a non-negative usage reading to a meter."""
        if not meter_id or not meter_id.strip():
            raise ValueError("Meter ID must not be empty.")
        if isinstance(units, bool) or not isinstance(units, (int, float)):
            raise TypeError("Units must be a number.")
        if units < 0:
            raise ValueError("Units must be non-negative.")

        self.meters[meter_id] = (
            self.meters.get(meter_id, 0.0) + units
        )
        LOGGER.info(
            "Recorded %.2f units for meter %s",
            units,
            meter_id,
        )

    def compute_bill(self, meter_id: str) -> float:
        """Compute a progressive three-tier electricity bill."""
        if meter_id not in self.meters:
            raise KeyError(f"Unknown meter ID: {meter_id}")

        units = self.meters[meter_id]
        tier1, tier2, tier3 = self.tier_rates

        if units <= 100:
            return units * tier1
        if units <= 300:
            return 100 * tier1 + (units - 100) * tier2

        return (
            100 * tier1
            + 200 * tier2
            + (units - 300) * tier3
        )

    def raise_rates(self, percent: float) -> None:
        """Increase all tariff rates by a non-negative percentage."""
        if isinstance(percent, bool) or not isinstance(
            percent, (int, float)
        ):
            raise TypeError("Percentage must be a number.")
        if percent < 0:
            raise ValueError("Percentage must be non-negative.")

        multiplier = 1 + percent / 100
        self.tier_rates = [
            rate * multiplier for rate in self.tier_rates
        ]

    def flag_spikes(self) -> list[str]:
        """Return meter IDs with unusually high usage."""
        return [
            meter_id
            for meter_id, units in self.meters.items()
            if units > SPIKE_LIMIT
        ]

    def load_meter_data(self, file: Path = DATA_FILE) -> None:
        """Load and validate saved meter totals."""
        try:
            with file.open("r", encoding="utf-8") as data_file:
                loaded = json.load(data_file)
        except FileNotFoundError:
            LOGGER.info(
                "No saved meter data found; starting with an empty store."
            )
            self.meters = {}
            return
        except (json.JSONDecodeError, OSError) as exc:
            LOGGER.error(
                "Could not load meter data from %s: %s",
                file,
                exc,
            )
            raise

        if not isinstance(loaded, dict):
            raise ValueError("Meter data must be a JSON object.")

        validated: dict[str, float] = {}
        for meter_id, units in loaded.items():
            if not isinstance(meter_id, str) or not meter_id.strip():
                raise ValueError("Meter IDs must be non-empty strings.")
            if (
                isinstance(units, bool)
                or not isinstance(units, (int, float))
                or units < 0
            ):
                raise ValueError(f"Invalid units for meter {meter_id}.")
            validated[meter_id] = float(units)

        self.meters = validated

    def save_meter_data(self, file: Path = DATA_FILE) -> None:
        """Save meter totals as JSON."""
        with file.open("w", encoding="utf-8") as data_file:
            json.dump(self.meters, data_file, indent=2)


def main() -> None:
    """Run a demonstration of meter tracking and billing."""
    system = EnergySystem()
    system.load_meter_data()

    system.record_reading("M-01", 120)
    system.record_reading("M-02", 640)
    system.record_reading("M-03", 0)

    LOGGER.info("Bill M-01: %.2f", system.compute_bill("M-01"))
    LOGGER.info("Bill M-03: %.2f", system.compute_bill("M-03"))
    LOGGER.info("High-usage meters: %s", system.flag_spikes())

    adjustment_text = (
        input("Extra units for M-01 (Enter for 0): ").strip() or "0"
    )

    try:
        adjustment = float(adjustment_text)
        system.record_reading("M-01", adjustment)
    except (ValueError, TypeError) as exc:
        LOGGER.error("Invalid adjustment: %s", exc)
        return

    system.save_meter_data()
    system.load_meter_data()

    LOGGER.info(
        "Bill M-01 after reload: %.2f",
        system.compute_bill("M-01"),
    )


if __name__ == "__main__":
    main()
