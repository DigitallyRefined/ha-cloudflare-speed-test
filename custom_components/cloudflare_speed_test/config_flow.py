"""Config flow for Cloudflare Speed Test."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, DEFAULT_SPEED_TEST_INTERVAL, CONF_SPEED_TEST_INTERVAL


class CloudflareSpeedTestFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle Cloudflare Speed Test config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            # Store the initial speed test interval in data (options can override later)
            return self.async_create_entry(
                title="Cloudflare Speed Test",
                data={CONF_SPEED_TEST_INTERVAL: user_input[CONF_SPEED_TEST_INTERVAL]},
            )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_SPEED_TEST_INTERVAL, default=DEFAULT_SPEED_TEST_INTERVAL
                ): vol.All(cv.positive_int, vol.Range(min=1, max=1440)),
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
        current = self.config_entry.options.get(
            CONF_SPEED_TEST_INTERVAL
        ) or self.config_entry.data.get(
            CONF_SPEED_TEST_INTERVAL, DEFAULT_SPEED_TEST_INTERVAL
        )

        schema = vol.Schema(
            {
                vol.Required(CONF_SPEED_TEST_INTERVAL, default=current): vol.All(
                    cv.positive_int, vol.Range(min=1, max=1440)
                ),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
