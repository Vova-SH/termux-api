"""Support for Termux numbers."""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .volume.coordinator import VolumeCoordinator
from .volume.entity import async_setup_number_entities
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Termux number."""
    coordinator: VolumeCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        VolumeCoordinator.__name__
    ]

    volumes = await async_setup_number_entities(coordinator)

    if volumes:
        async_add_entities(volumes)
