"""Base Battery Entities for Home Assitant."""
from homeassistant.const import (PERCENTAGE, TEMP_CELSIUS)
from homeassistant.components.sensor import (SensorEntity, SensorDeviceClass, SensorStateClass)

from ..base.entity import BaseCoordinatorEntity
from .coordinator import BatteryCoordinator

async def async_setup_sensor_entities(coordinator: BatteryCoordinator) -> list[SensorEntity]:
    """Setup Battery sensors"""
    await coordinator.async_config_entry_first_refresh()

    return [
        BatteryPercentage(coordinator),
        BatteryHealth(coordinator),
        BatteryTemperature(coordinator),
        BatteryPlug(coordinator),
        BatteryStatus(coordinator)
    ]

class BaseBatteryEntity(BaseCoordinatorEntity, SensorEntity):
    """Base Battery entity"""
    coordinator: BatteryCoordinator

    def __init__(
        self,
        coordinator: BatteryCoordinator,
        postfixName: str
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"id_Battery{postfixName}"
        self._attr_name = f"Battery {postfixName}"

class BatteryTemperature(BaseBatteryEntity):
    """Battery Temperature entity"""
    _attr_icon = "mdi:battery"
    _attr_unit_of_measurement = TEMP_CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: BatteryCoordinator) -> None:
        super().__init__(coordinator, "Temperature")

    def _create_device(self):
        self._state = round(self.coordinator.data.temperature, 1)

class BatteryStatus(BaseBatteryEntity):
    """Battery Status entity"""
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: BatteryCoordinator) -> None:
        super().__init__(coordinator, "Status")

    @property
    def icon(self):
        status = self._state
        match status:
            case "CHARGING":
                return "mdi:battery-plus"
            case "DISCHARGING":
                return "mdi:battery-minus"
            case "FULL":
                return "mdi:battery"
            case "NOT_CHARGING":
                return "mdi:battery-off"
            case _:
                return "mdi:battery-unknown"

    @property
    def state(self):
        return self._state

    def _create_device(self):
        self._state = self.coordinator.data.status

class BatteryPlug(BaseBatteryEntity):
    """Battery Plug entity"""
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: BatteryCoordinator) -> None:
        super().__init__(coordinator, "Plug")

    @property
    def icon(self):
        plugged = self._state
        match plugged:
            case "UNPLUGGED":
                return "mdi:power-plug-off"
            case "PLUGGED_AC":
                return "mdi:power-plug"
            case "PLUGGED_USB":
                return "mdi:usb-port"
            case "PLUGGED_WIRELESS":
                return "mdi:battery-charging-wireless"
            case _:
                return "mdi:battery-unknown"

    def _create_device(self):
        self._state = self.coordinator.data.plugged

class BatteryPercentage(BaseBatteryEntity):
    """Battery Percentage entity"""
    _attr_unit_of_measurement = PERCENTAGE
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: BatteryCoordinator) -> None:
        super().__init__(coordinator, "Percentage")

    @property
    def icon(self):
        data = self._data
        percentage = int(data.percentage / 10) * 10
        if percentage == 0:
            percentage = 10


        plugged = data.plugged
        if data.status != "CHARGING":
            return self._icon_percent("mdi:battery", percentage)
        else:
            match plugged:
                case "PLUGGED_AC" | "PLUGGED_USB":
                    return self._icon_percent("mdi:battery-charging", percentage)
                case "PLUGGED_WIRELESS":
                    return self._icon_percent("mdi:battery-charging-wireless", percentage)
                case _:
                    return self._icon_percent("mdi:battery", percentage)

        return self._icon_percent("mdi:battery", percentage)

    def _create_device(self):
        self._data = self.coordinator.data
        self._state = self._data.percentage

    def _icon_percent(self, prefix: str, percentage: int):
        return prefix if percentage == 100 else (prefix + "-" + str(percentage))

class BatteryHealth(BaseBatteryEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, coordinator: BatteryCoordinator) -> None:
        super().__init__(coordinator, "Health")

    @property
    def icon(self):
        health = self._state
        match health:
            case "GOOD":
                return "mdi:battery-heart-variant"
            case "DEAD":
                return "mdi:battery-off"
            case "COLD":
                return "mdi:snowflake-alert"
            case "OVERHEAT":
                return "mdi:fire-alert"
            case "OVER_VOLTAGE":
                return "mdi:flash-alert"
            case _:
                return "mdi:battery-unknown"

    def _create_device(self):
        self._state = self.coordinator.data.health