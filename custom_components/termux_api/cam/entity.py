"""Base Camera Entities for Home Assitant."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.components.switch import SwitchEntity
from homeassistant.components.camera import CameraEntityFeature, Camera

from .data import CameraDto
from .coordinator import CameraCoordinator
from ..base.entity import BaseCoordinatorEntity


async def async_setup_camera_entities(coordinator: CameraCoordinator) -> list[Camera]:
    """Setup Camera cameras"""
    await coordinator.async_config_entry_first_refresh()

    return list(map(lambda dto: CameraEntity(coordinator, dto.id), coordinator.data))


async def async_setup_switch_entities(
    coordinator: CameraCoordinator,
) -> list[SwitchEntity]:
    """Setup Camera switches"""
    await coordinator.async_config_entry_first_refresh()

    return list(
        map(lambda dto: CameraSwitchEntity(coordinator, dto.id), coordinator.data)
    )


class CameraEntity(Camera, BaseCoordinatorEntity):
    """Camera entity"""

    coordinator: CameraCoordinator

    _update_interval_off = timedelta(days=1).total_seconds()
    _update_interval_on = timedelta(seconds=10).total_seconds()

    _attr_frame_interval = _update_interval_off
    _attr_supported_features = CameraEntityFeature.ON_OFF
    _attr_should_poll = False
    _attr_is_on = True

    def __init__(self, coordinator: CameraCoordinator, camera_id: int) -> None:
        self._id = camera_id
        self._data = coordinator.get_camera(camera_id)

        self._attr_unique_id = f"id_Camera{self._data.facing.title()}{self._data.id}"
        self._attr_name = f"{self._data.facing.title()} camera"

        Camera.__init__(self)
        BaseCoordinatorEntity.__init__(self, coordinator)

    @property
    def icon(self):
        if self._data.is_on:
            return "mdi:camera"
        return "mdi:camera-off"

    async def async_camera_image(self, width=None, height=None):
        return await self.coordinator.take_photo(self._data.id, width, height)

    async def async_turn_off(self):
        await self.coordinator.set_camera_on(self._data.id, False)
        self._attr_frame_interval = self._update_interval_off

    async def async_turn_on(self):
        await self.coordinator.set_camera_on(self._data.id, True)
        self._attr_frame_interval = self._update_interval_on

    def _create_device(self):
        self._data: CameraDto = self.coordinator.get_camera(self._id)
        if self._data.is_on:
            self._attr_frame_interval = self._update_interval_on
        else:
            self._attr_frame_interval = self._update_interval_off


class CameraSwitchEntity(SwitchEntity, BaseCoordinatorEntity):
    """Switch Camera entity"""

    coordinator: CameraCoordinator

    def __init__(self, coordinator: CameraCoordinator, camera_id: int) -> None:
        self._id = camera_id
        self._data = coordinator.get_camera(camera_id)
        self._attr_is_on = self._data.is_on

        self._attr_unique_id = (
            f"id_CameraSwitch{self._data.facing.title()}{self._data.id}"
        )
        self._attr_name = f"Switch {self._data.facing.title()} camera"

        SwitchEntity.__init__(self)
        BaseCoordinatorEntity.__init__(self, coordinator)

    async def async_turn_on(self, **kwargs):
        await self.coordinator.set_camera_on(self._data.id, True)
        self._attr_is_on = True

    async def async_turn_off(self, **kwargs):
        await self.coordinator.set_camera_on(self._data.id, False)
        self._attr_is_on = False

    def _create_device(self):
        self._data: CameraDto = self.coordinator.get_camera(self._id)
        self._attr_is_on = self._data.is_on
