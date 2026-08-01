"""Config flow for Cloudflare Speed Test."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_CONNECTION_TIMEOUT,
    CONF_READ_TIMEOUT,
    CONF_SPEED_TEST_INTERVAL,
    CONF_TESTS,
    DEFAULT_CONNECTION_TIMEOUT,
    DEFAULT_READ_TIMEOUT,
    DEFAULT_SPEED_TEST_INTERVAL,
    DEFAULT_TESTS,
    DOMAIN,
    TEST_OPTIONS,
)


def _tests_selector() -> SelectSelector:
    """Return the multi-select used to pick which tests to run."""
    return SelectSelector(
        SelectSelectorConfig(
            options=list(TEST_OPTIONS),
            multiple=True,
            mode=SelectSelectorMode.LIST,
            translation_key="tests",
        )
    )


def _tests_field(default: list[str] | tuple[str, ...]) -> vol.Optional:
    """Return the schema field used to pick which tests to run."""
    return vol.Optional(CONF_TESTS, default=list(default))


class CloudflareSpeedTestFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle Cloudflare Speed Test config flow."""

    VERSION = 2

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        if user_input is not None:
            if not user_input.get(CONF_TESTS):
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._user_schema(),
                    errors={CONF_TESTS: "select_at_least_one_test"},
                )
            # Store the initial configuration in data (options can override later)
            return self.async_create_entry(
                title="Cloudflare Speed Test",
                data={
                    CONF_SPEED_TEST_INTERVAL: user_input[CONF_SPEED_TEST_INTERVAL],
                    CONF_CONNECTION_TIMEOUT: user_input[CONF_CONNECTION_TIMEOUT],
                    CONF_READ_TIMEOUT: user_input[CONF_READ_TIMEOUT],
                    CONF_TESTS: user_input[CONF_TESTS],
                },
            )

        return self.async_show_form(step_id="user", data_schema=self._user_schema())

    @staticmethod
    def _user_schema() -> vol.Schema:
        """Build the initial setup form schema."""
        return vol.Schema(
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
                _tests_field(DEFAULT_TESTS): _tests_selector(),
            }
        )

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
            if not user_input.get(CONF_TESTS):
                return self.async_show_form(
                    step_id="init",
                    data_schema=self._options_schema(),
                    errors={CONF_TESTS: "select_at_least_one_test"},
                )
            # Save as options
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(step_id="init", data_schema=self._options_schema())

    def _options_schema(self) -> vol.Schema:
        """Build the options form schema, pre-filled from options → data → default."""
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
        current_tests = self.config_entry.options.get(
            CONF_TESTS
        ) or self.config_entry.data.get(CONF_TESTS, DEFAULT_TESTS)

        return vol.Schema(
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
                _tests_field(current_tests): _tests_selector(),
            }
        )
