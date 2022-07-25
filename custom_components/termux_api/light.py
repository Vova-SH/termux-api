"""Support for Termux lights."""
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .termux import TermuxAPI
from .brightness.entity import setup_lights_entities
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Termux light."""
    api: TermuxAPI = hass.data[DOMAIN][config_entry.entry_id][TermuxAPI.__name__]

    async_add_entities(setup_lights_entities(api))
