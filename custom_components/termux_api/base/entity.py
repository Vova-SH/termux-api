"""Termux:API Home Assistant Base Device Model."""
from abc import abstractmethod

from homeassistant.core import callback
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from ..const import DEVICE


class BaseEntity(Entity):
    """Termux base entity."""

    _attr_device_info = DEVICE


class BaseCoordinatorEntity(CoordinatorEntity, BaseEntity):
    """Termux base coordinator."""

    def __init__(self, coordinator: DataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._create_device()

    @property
    def state(self):
        if hasattr(self, "_state"):
            return self._state
        return "unknown"

    async def async_update(self):
        if not self.enabled:
            return

        await self.coordinator.async_request_refresh()

    @callback
    def _handle_coordinator_update(self):
        self._create_device()
        super()._handle_coordinator_update()

    @abstractmethod
    def _create_device(self):
        """Update the device with the latest data."""
