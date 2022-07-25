"""Base Volume Coordinator for Home Assitant."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from ..termux import TermuxAPI
from .data import VolumeDto

_LOGGER = logging.getLogger(__name__)


class VolumeCoordinator(DataUpdateCoordinator):
    """Base Volume Coordinator"""

    def __init__(self, hass: HomeAssistant, api: TermuxAPI) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Volume coordinator",
            update_interval=timedelta(days=7),
        )

        self.api = api
        self.data: list[VolumeDto] = []

    def get_volume(self, stream: str) -> VolumeDto:
        """Return volume info by stream"""
        volume_dto: VolumeDto = next(
            filter(lambda dto: dto.stream == stream, self.data), None
        )
        if not volume_dto:
            return VolumeDto()
        return volume_dto

    async def set_value(self, stream: str, value: int):
        """Update volume value by stream"""
        volume_dto: VolumeDto = next(
            filter(lambda dto: dto.stream == stream, self.data), None
        )
        if not volume_dto:
            return
        await self.api.set_volume(stream, value)
        volume_dto.value = value
        await self.async_request_refresh()

    async def _async_update_data(self) -> list[VolumeDto]:
        return await self.api.get_volumes()
