"""Provide Termux:API"""
from __future__ import annotations

from functools import partial
import os
import subprocess
import json
import logging
import async_timeout
import asyncio

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import PlatformNotReady

from .battery.data import BatteryDto
from .volume.data import VolumeDto
from .cam.data import CameraDto

_LOGGER = logging.getLogger(__name__)


class TermuxAPI:
    """Termux API"""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass

    async def get_battery(self) -> BatteryDto:
        """Return current status of battery."""
        return BatteryDto.from_json(
            json.loads(await self._run_command(["termux-battery-status"]))
        )

    async def get_volumes(self) -> list[VolumeDto]:
        """Return current status of volumes sounds stream."""
        volumes_json = json.loads(await self._run_command(["termux-volume"]))
        return list(map(VolumeDto.from_json, volumes_json))

    async def set_volume(self, stream: str, value: int) -> None:
        """Update volume for sound stream."""
        await self._run_command(["termux-volume", stream, str(value)])

    async def set_brightness(self, value: int) -> None:
        """Set brightness screen."""
        await self._run_command(["termux-brightness", str(value)])

    async def set_brightness_auto(self) -> None:
        """Set auto brightness screen."""
        await self._run_command(["termux-brightness", "auto"])

    async def get_cameras(self) -> list[CameraDto]:
        """Return current cameras info."""
        response = json.loads(await self._run_command(["termux-camera-info"]))
        return list(map(CameraDto.from_json, response))

    async def take_camera_photo(self, camera_id: int) -> bytes:
        """Return current capture from camera."""
        output_path = f"{os.environ['HOME']}/.homeassistant/photos/{camera_id}.jpg"
        await self._run_command(
            ["termux-camera-photo", "-c", str(camera_id), output_path]
        )
        with open(output_path, "rb") as file:
            return file.read()

    async def _run_command(self, args):
        try:
            async with async_timeout.timeout(10):
                result = await self.hass.async_add_executor_job(
                    partial(
                        subprocess.run,
                        args,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        encoding="utf-8",
                    )
                )
                if result.returncode == 0:
                    return result.stdout
                _LOGGER.warning('Command "%s" error: %s', args[0], result.stderr)
                raise PlatformNotReady
        except asyncio.TimeoutError as error:
            _LOGGER.warning('Command "%s" run over 10 seconds and canceling', args[0])
            raise PlatformNotReady from error
