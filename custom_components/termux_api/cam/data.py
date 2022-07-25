"""Base Camera data sources for Home Assitant."""
from dataclasses import dataclass


@dataclass
class CameraDto:
    """Camera info."""

    id: int = 0
    facing: str = "UNKNOWN"
    is_on: bool = False

    @classmethod
    def from_json(cls, json):
        """Parse JSON to Camera DTO"""
        return cls(json["id"], json["facing"], False)
