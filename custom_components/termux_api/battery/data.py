"""Base Battery data sources for Home Assitant."""
from dataclasses import dataclass


@dataclass
class BatteryDto:
    """Battery info."""

    health: str = (
        "UNKNOWN"  # GOOD DEAD COLD OVERHEAT OVER_VOLTAGE UNKNOWN UNSPECIFIED_FAILURE
    )
    percentage: int = 100
    plugged: str = "UNKNOWN"  # UNPLUGGED PLUGGED_AC PLUGGED_USB PLUGGED_WIRELESS
    status: str = "UNKNOWN"  # CHARGING DISCHARGING FULL NOT_CHARGING UNKNOWN
    temperature: float = 0.0
    current: int = 0

    @classmethod
    def from_json(cls, json):
        """Parse JSON to Battery DTO"""
        return cls(
            json["health"],
            json["percentage"],
            json["plugged"],
            json["status"],
            json["temperature"],
            json["current"],
        )
