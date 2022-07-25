"""Constants for the Termux:API integration."""
from homeassistant.helpers.entity import DeviceInfo

DOMAIN = "termux_api"
DEVICE: DeviceInfo = {
    "identifiers": {(DOMAIN, "Termux:API Device")},
    "name": "Termux:API",
    "model": "termux",
    "manufacturer": "termux",
}
