"""Support for Termux cameras."""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .cam.entity import async_setup_camera_entities
from .cam.coordinator import CameraCoordinator
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Termux camera."""
    coordinator: CameraCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        CameraCoordinator.__name__
    ]

    cameras = await async_setup_camera_entities(coordinator)

    if cameras:
        async_add_entities(cameras)
