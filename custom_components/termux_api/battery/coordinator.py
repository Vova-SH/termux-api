"""Base Battery Coordinator for Home Assitant."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from ..termux import TermuxAPI
from .data import BatteryDto

_LOGGER = logging.getLogger(__name__)


class BatteryCoordinator(DataUpdateCoordinator):
    """Base Battery Coordinator"""

    data: BatteryDto

    def __init__(self, hass: HomeAssistant, api: TermuxAPI) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Battery coordinator",
            update_interval=timedelta(minutes=5),
        )

        self.api = api
        self.data = BatteryDto()

    async def _async_update_data(self) -> BatteryDto:
        return await self.api.get_battery()
