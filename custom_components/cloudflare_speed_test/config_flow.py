"""Config flow for Cloudflare Speed Test."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from homeassistant.config_entries import ConfigEntry

from .const import (
    CONF_CONNECTION_TIMEOUT,
    CONF_READ_TIMEOUT,
    CONF_SPEED_TEST_INTERVAL,
    DEFAULT_CONNECTION_TIMEOUT,
    DEFAULT_READ_TIMEOUT,
    DEFAULT_SPEED_TEST_INTERVAL,
    DOMAIN,
)


class CloudflareSpeedTestFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle Cloudflare Speed Test config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            # Store the initial configuration in data (options can override later)
            return self.async_create_entry(
                title="Cloudflare Speed Test",
                data={
                    CONF_SPEED_TEST_INTERVAL: user_input[CONF_SPEED_TEST_INTERVAL],
                    CONF_CONNECTION_TIMEOUT: user_input[CONF_CONNECTION_TIMEOUT],
                    CONF_READ_TIMEOUT: user_input[CONF_READ_TIMEOUT],
                },
            )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_SPEED_TEST_INTERVAL, default=DEFAULT_SPEED_TEST_INTERVAL
                ): vol.All(cv.positive_int, vol.Range(min=10, max=1440)),
                vol.Required(
                    CONF_CONNECTION_TIMEOUT, default=DEFAULT_CONNECTION_TIMEOUT
                ): vol.All(cv.positive_int, vol.Range(min=5, max=300)),
                vol.Required(CONF_READ_TIMEOUT, default=DEFAULT_READ_TIMEOUT): vol.All(
                    cv.positive_int, vol.Range(min=10, max=600)
                ),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        return CloudflareSpeedTestOptionsFlowHandler(config_entry)


class CloudflareSpeedTestOptionsFlowHandler(config_entries.OptionsFlowWithConfigEntry):
    """Handle options flow for Cloudflare Speed Test."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        super().__init__(config_entry)

    async def async_step_init(self, user_input=None):
        """Manage the Cloudflare Speed Test options."""
        if user_input is not None:
            # Save as options
            return self.async_create_entry(title="", data=user_input)

        # Pre-fill from options → data → default
        current_interval = self.config_entry.options.get(
            CONF_SPEED_TEST_INTERVAL
        ) or self.config_entry.data.get(
            CONF_SPEED_TEST_INTERVAL, DEFAULT_SPEED_TEST_INTERVAL
        )
        current_connection_timeout = self.config_entry.options.get(
            CONF_CONNECTION_TIMEOUT
        ) or self.config_entry.data.get(
            CONF_CONNECTION_TIMEOUT, DEFAULT_CONNECTION_TIMEOUT
        )
        current_read_timeout = self.config_entry.options.get(
            CONF_READ_TIMEOUT
        ) or self.config_entry.data.get(CONF_READ_TIMEOUT, DEFAULT_READ_TIMEOUT)

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_SPEED_TEST_INTERVAL, default=current_interval
                ): vol.All(cv.positive_int, vol.Range(min=10, max=1440)),
                vol.Required(
                    CONF_CONNECTION_TIMEOUT, default=current_connection_timeout
                ): vol.All(cv.positive_int, vol.Range(min=5, max=300)),
                vol.Required(CONF_READ_TIMEOUT, default=current_read_timeout): vol.All(
                    cv.positive_int, vol.Range(min=10, max=600)
                ),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
