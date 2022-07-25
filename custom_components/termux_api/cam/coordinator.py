"""Base Camera Coordinator for Home Assitant."""
from __future__ import annotations

from datetime import timedelta
import os
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from ..termux import TermuxAPI
from .data import CameraDto

_LOGGER = logging.getLogger(__name__)


class CameraCoordinator(DataUpdateCoordinator):
    """Base Camera Coordinator"""

    data: list[CameraDto]

    _placeholder_path: str = (
        f"{os.environ['HOME']}/.homeassistant/custom_components/termux_api/placeholder.jpg"
    )

    def __init__(self, hass: HomeAssistant, api: TermuxAPI) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Camera coordinator",
            update_interval=timedelta(days=7),
        )

        self.api = api
        self.data: list[CameraDto] = []

    async def take_photo(
        self, camera_id: int, width: int | None = None, height: int | None = None
    ) -> bytes:
        """Return photo from camera by id"""
        camera_dto: CameraDto = next(
            filter(lambda dto: dto.id == camera_id, self.data), None
        )
        if not camera_dto:
            return
        if camera_dto.is_on:
            return await self.api.take_camera_photo(camera_id)
        return await self._get_placeholder()

    def get_camera(self, camera_id: int) -> CameraDto:
        """Return camera info by id"""
        camera_dto: CameraDto = next(
            filter(lambda dto: dto.id == camera_id, self.data), None
        )
        if camera_dto:
            return camera_dto
        _LOGGER.warning("Camera %s Not Found", camera_dto.id)
        return CameraDto()

    async def set_camera_on(self, camera_id: int, is_on: bool) -> None:
        """Set camera enable"""
        await self.hass.async_add_executor_job(self._set_camera_on, camera_id, is_on)
        await self.async_request_refresh()

    async def _async_update_data(self) -> list[CameraDto]:
        if self.data:
            return self.data
        return await self.api.get_cameras()

    def _set_camera_on(self, camera_id: int, is_on: bool):
        camera_dto: CameraDto = next(
            filter(lambda dto: dto.id == camera_id, self.data), None
        )
        if not camera_dto:
            return
        camera_dto.is_on = is_on

    async def _get_placeholder(self) -> bytes:
        with open(self._placeholder_path, "rb") as file:
            return file.read()
