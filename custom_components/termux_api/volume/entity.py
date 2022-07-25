"""Base Volume Entities for Home Assitant."""
from homeassistant.components.number import (
    NumberMode,
    NumberEntity
)

from ..base.entity import BaseCoordinatorEntity
from .coordinator import VolumeCoordinator

async def async_setup_number_entities(coordinator: VolumeCoordinator) -> list[NumberEntity]:
    """Setup Volume numbers"""
    await coordinator.async_config_entry_first_refresh()

    return list(map(lambda dto: VolumeEntity(coordinator, dto.stream), coordinator.data))

class VolumeEntity(BaseCoordinatorEntity, NumberEntity):
    """Base Volume entity"""
    coordinator: VolumeCoordinator

    _attr_native_step = 1.0
    _attr_native_min_value = 0.0
    _attr_mode = NumberMode.SLIDER

    def __init__(
        self,
        coordinator: VolumeCoordinator,
        stream: str
    ) -> None:
        self._stream = stream
        self._data = coordinator.get_volume(stream)
        self._attr_unique_id = f"id_Volume{self._data.stream.title()}"
        self._attr_name = f"{self._data.stream.title()} volume"

        super().__init__(coordinator)

    @property
    def icon(self):
        stream = self._data.stream
        volume = self._state
        match stream:
            case "call":
                return "mdi:phone" if volume > 0 else "mdi:phone-off"
            case "system":
                return "mdi:cog" if volume > 0 else "mdi:cog-off"
            case "ring":
                return "mdi:volume-high" if volume > 0 else "mdi:volume-off"
            case "music":
                return "mdi:music-note" if volume > 0 else "mdi:music-note-off"
            case "alarm":
                return "mdi:alarm-note" if volume > 0 else "mdi:alarm-note-off"
            case "notification":
                return "mdi:bell-ring" if volume > 0 else "mdi:bell-off"
            case _:
                return "mdi:volume-high" if volume > 0 else "mdi:volume-off"

    async def async_set_native_value(self, value: float) -> None:
        await self.coordinator.set_value(self._data.stream, int(value))

    def _create_device(self):
        self._data = self.coordinator.get_volume(self._stream)
        self._state = self._data.volume
        self._attr_native_max_value = self._data.max_volume