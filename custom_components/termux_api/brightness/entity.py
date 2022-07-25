"""Base Brightness Entities for Home Assitant."""
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    SUPPORT_BRIGHTNESS,
    ColorMode,
    LightEntity,
)

from ..base.entity import BaseEntity
from ..termux import TermuxAPI


def setup_lights_entities(api: TermuxAPI) -> list[LightEntity]:
    """Setup Brightness lights"""
    return [BrightnessEntity(api)]


class BrightnessEntity(BaseEntity, LightEntity, RestoreEntity):
    """Brightness entity"""

    _attr_icon = "mdi:lightbulb"
    _attr_unique_id = "id_LightBrightness"
    _attr_name = "Brightness screen"

    _attr_color_mode = ColorMode.BRIGHTNESS
    color_modes = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}
    supported_color_modes = {ColorMode.BRIGHTNESS}
    supported_features = SUPPORT_BRIGHTNESS
    brightness = 0
    is_on = False

    def __init__(self, api: TermuxAPI) -> None:
        self.api = api

    async def async_turn_on(self, **kwargs):
        self.is_on = True
        if ATTR_BRIGHTNESS in kwargs:
            brightness = int(kwargs[ATTR_BRIGHTNESS])
            self.brightness = brightness
            await self.api.set_brightness(brightness)

    async def async_turn_off(self, **kwargs):
        self.is_on = False
        self.brightness = 0
        await self.api.set_brightness_auto()

    async def async_added_to_hass(self):
        await super().async_added_to_hass()
        state = await self.async_get_last_state()
        if not state:
            return

        self.is_on = state.state
        if "brightness" in state.attributes:
            self.brightness = state.attributes["brightness"]
