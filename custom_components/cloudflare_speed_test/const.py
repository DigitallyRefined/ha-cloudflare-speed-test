"""Constants used by Cloudflare Speed Test."""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "cloudflare_speed_test"

ATTR_SERVER_REGION: Final = "server_region"
ATTR_SERVER_CODE: Final = "server_code"
ATTR_SERVER_CITY: Final = "server_city"

DEFAULT_NAME: Final = "Cloudflare Speed Test"

# Default speed test interval in minutes (used if nothing set in config entry)
DEFAULT_SPEED_TEST_INTERVAL: Final = 60

# Options / config keys
CONF_SPEED_TEST_INTERVAL: Final = "speed_test_interval"

ATTRIBUTION: Final = "Data retrieved from Cloudflare Speed Test"
