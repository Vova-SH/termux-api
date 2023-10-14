"""Support Termux:API"""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MAJOR_VERSION, MINOR_VERSION
from homeassistant.core import HomeAssistant

from .termux import TermuxAPI
from .battery.coordinator import BatteryCoordinator
from .cam.coordinator import CameraCoordinator
from .volume.coordinator import VolumeCoordinator
from .const import DOMAIN

PLATFORMS: list[str] = ["sensor", "number", "light", "camera", "switch"]

async def async_setup(hass: HomeAssistant, hass_config: dict):
    assert (MAJOR_VERSION, MINOR_VERSION) >= (2021, 12)

    api = TermuxAPI(hass)
    values = [
        api,
        BatteryCoordinator(hass, api),
        CameraCoordinator(hass, api),
        VolumeCoordinator(hass, api),
    ]
    keys = list(map(lambda obj: type(obj).__name__, values))

    hass.data[DOMAIN] = hass_config.get(DOMAIN) or {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Async setup hass config entry."""
    api = TermuxAPI(hass)
    values = [
        api,
        BatteryCoordinator(hass, api),
        CameraCoordinator(hass, api),
        VolumeCoordinator(hass, api),
    ]
    keys = list(map(lambda obj: type(obj).__name__, values))

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = dict(zip(keys, values))

    for domain in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, domain)
        )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unloading the Termux platforms."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
