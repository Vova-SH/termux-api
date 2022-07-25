"""Support for Termux sensors."""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .battery.coordinator import BatteryCoordinator
from .battery.entity import async_setup_sensor_entities
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Termux sensor."""
    coordinator: BatteryCoordinator = hass.data[DOMAIN][config_entry.entry_id][
        BatteryCoordinator.__name__
    ]

    battery_entities = await async_setup_sensor_entities(coordinator)

    async_add_entities(battery_entities)
