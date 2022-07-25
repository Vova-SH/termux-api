"""Base Volume data sources for Home Assitant."""
from dataclasses import dataclass


@dataclass
class VolumeDto:
    """Volume info."""

    stream: str = "UNKNOWN"
    volume: int = 0
    max_volume: int = 0

    @classmethod
    def from_json(cls, json):
        """Parse JSON to Volume DTO"""
        return cls(json["stream"], json["volume"], json["max_volume"])
