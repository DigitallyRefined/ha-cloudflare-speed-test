"""Coordinator for cloudflare_speed_test."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any, cast

from cfspeedtest import CloudflareSpeedtest, TestSpec, TestType
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_CONNECTION_TIMEOUT,
    CONF_READ_TIMEOUT,
    CONF_TESTS,
    DEFAULT_CONNECTION_TIMEOUT,
    DEFAULT_READ_TIMEOUT,
    DEFAULT_SPEED_TEST_INTERVAL,
    DEFAULT_TESTS,
    DOMAIN,
    TEST_DOWNLOAD_1MB,
    TEST_DOWNLOAD_10MB,
    TEST_DOWNLOAD_25MB,
    TEST_DOWNLOAD_100KB,
    TEST_LATENCY,
    TEST_UPLOAD_1MB,
    TEST_UPLOAD_10MB,
    TEST_UPLOAD_100KB,
)

_LOGGER = logging.getLogger(__name__)

type CloudflareSpeedTestConfigEntry = ConfigEntry[CloudflareSpeedTestDataCoordinator]

# Map config test keys to the underlying cfspeedtest specifications
TEST_SPECS: dict[str, TestSpec] = {
    TEST_LATENCY: TestSpec(1, 20, "latency", TestType.Down),
    TEST_DOWNLOAD_100KB: TestSpec(100_000, 10, "100kB", TestType.Down),
    TEST_DOWNLOAD_1MB: TestSpec(1_000_000, 8, "1MB", TestType.Down),
    TEST_DOWNLOAD_10MB: TestSpec(10_000_000, 6, "10MB", TestType.Down),
    TEST_DOWNLOAD_25MB: TestSpec(25_000_000, 4, "25MB", TestType.Down),
    TEST_UPLOAD_100KB: TestSpec(100_000, 8, "100kB", TestType.Up),
    TEST_UPLOAD_1MB: TestSpec(1_000_000, 6, "1MB", TestType.Up),
    TEST_UPLOAD_10MB: TestSpec(10_000_000, 4, "10MB", TestType.Up),
}


def build_tests(enabled: list[str] | tuple[str, ...]) -> tuple[TestSpec, ...]:
    """Build test specifications for the enabled tests, in the default order."""
    enabled_set = set(enabled)
    return tuple(TEST_SPECS[key] for key in DEFAULT_TESTS if key in enabled_set)


class CloudflareSpeedTestDataCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Get the latest data from Cloudflare Speed Test."""

    config_entry: CloudflareSpeedTestConfigEntry

    @property
    def enabled_tests(self) -> list[str] | tuple[str, ...]:
        """Return the tests enabled for this config entry."""
        return self._enabled_tests

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: CloudflareSpeedTestConfigEntry,
        api: CloudflareSpeedtest,
        *,
        speed_test_interval_minutes: int | None = None,
    ) -> None:
        """Initialize the data object."""
        self.hass = hass

        # Get timeout values from options → data → defaults
        self._connection_timeout = config_entry.options.get(
            CONF_CONNECTION_TIMEOUT
        ) or config_entry.data.get(CONF_CONNECTION_TIMEOUT, DEFAULT_CONNECTION_TIMEOUT)
        self._read_timeout = config_entry.options.get(
            CONF_READ_TIMEOUT
        ) or config_entry.data.get(CONF_READ_TIMEOUT, DEFAULT_READ_TIMEOUT)

        # Get the enabled tests from options → data → all tests
        self._enabled_tests = config_entry.options.get(
            CONF_TESTS
        ) or config_entry.data.get(CONF_TESTS, DEFAULT_TESTS)

        self._api_cls = api
        self.api: CloudflareSpeedtest | None = None

        minutes = speed_test_interval_minutes or DEFAULT_SPEED_TEST_INTERVAL

        super().__init__(
            self.hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=timedelta(minutes=minutes),
        )

    def update_data(self) -> dict[str, Any]:
        """Get the latest data from Cloudflare Speed Test."""
        if self.api is None:
            self.api = self._api_cls(
                timeout=(self._connection_timeout, self._read_timeout),
                tests=build_tests(self._enabled_tests),
            )
        results = self.api.run_all()
        return cast(dict[str, Any], results)

    async def _async_update_data(self) -> dict[str, Any]:
        """Update CloudflareSpeedTest data."""
        return await self.hass.async_add_executor_job(self.update_data)
