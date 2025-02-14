"""Coordinator for cloudflare_speed_test."""

from datetime import timedelta
import logging
from typing import Any, cast

import speedtest as cloudflarespeedtest

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_SERVER_ID, DEFAULT_SCAN_INTERVAL, DEFAULT_SERVER, DOMAIN

_LOGGER = logging.getLogger(__name__)

type CloudflareSpeedTestConfigEntry = ConfigEntry[CloudflareSpeedTestDataCoordinator]


class CloudflareSpeedTestDataCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Get the latest data from Cloudflare Speed Test."""

    config_entry: CloudflareSpeedTestConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: CloudflareSpeedTestConfigEntry,
        api: cloudflarespeedtest.Speedtest,
    ) -> None:
        """Initialize the data object."""
        self.hass = hass
        self.api = api
        self.servers: dict[str, dict] = {DEFAULT_SERVER: {}}
        super().__init__(
            self.hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=timedelta(minutes=DEFAULT_SCAN_INTERVAL),
        )

    def update_servers(self) -> None:
        """Update list of test servers."""
        test_servers = self.api.get_servers()
        test_servers_list = [
            server for servers in test_servers.values() for server in servers
        ]
        for server in sorted(
            test_servers_list,
            key=lambda server: (
                server["country"],
                server["name"],
                server["sponsor"],
            ),
        ):
            self.servers[
                f"{server['country']} - {server['sponsor']} - {server['name']}"
            ] = server

    def update_data(self) -> dict[str, Any]:
        """Get the latest data from Cloudflare Speed Test."""
        self.update_servers()
        self.api.closest.clear()
        if self.config_entry.options.get(CONF_SERVER_ID):
            server_id = self.config_entry.options.get(CONF_SERVER_ID)
            self.api.get_servers(servers=[server_id])

        best_server = self.api.get_best_server()
        _LOGGER.debug(
            "Executing Cloudflare Speed Test speed test with server_id: %s",
            best_server["id"],
        )
        self.api.download()
        self.api.upload()
        return cast(dict[str, Any], self.api.results.dict())

    async def _async_update_data(self) -> dict[str, Any]:
        """Update CloudflareSpeedTest data."""
        try:
            return await self.hass.async_add_executor_job(self.update_data)
        except cloudflarespeedtest.NoMatchedServers as err:
            raise UpdateFailed("Selected server is not found.") from err
        except cloudflarespeedtest.SpeedTestException as err:
            raise UpdateFailed(err) from err
