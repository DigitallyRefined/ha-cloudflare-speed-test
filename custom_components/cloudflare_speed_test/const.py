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
CONF_CONNECTION_TIMEOUT: Final = "connection_timeout"
CONF_READ_TIMEOUT: Final = "read_timeout"
CONF_TESTS: Final = "tests"

# Timeout settings in seconds
# Set high enough to support slow 1Mbps connections (25MB file = ~200s at 1Mbps)
DEFAULT_CONNECTION_TIMEOUT: Final = 30
DEFAULT_READ_TIMEOUT: Final = 300
DEFAULT_TIMEOUT: Final = (DEFAULT_CONNECTION_TIMEOUT, DEFAULT_READ_TIMEOUT)

# Individual speed tests that can be enabled or disabled
TEST_LATENCY: Final = "latency"
TEST_DOWNLOAD_100KB: Final = "download_100kb"
TEST_DOWNLOAD_1MB: Final = "download_1mb"
TEST_DOWNLOAD_10MB: Final = "download_10mb"
TEST_DOWNLOAD_25MB: Final = "download_25mb"
TEST_UPLOAD_100KB: Final = "upload_100kb"
TEST_UPLOAD_1MB: Final = "upload_1mb"
TEST_UPLOAD_10MB: Final = "upload_10mb"

TEST_OPTIONS: Final = (
    TEST_LATENCY,
    TEST_DOWNLOAD_100KB,
    TEST_DOWNLOAD_1MB,
    TEST_DOWNLOAD_10MB,
    TEST_DOWNLOAD_25MB,
    TEST_UPLOAD_100KB,
    TEST_UPLOAD_1MB,
    TEST_UPLOAD_10MB,
)

# All available tests, enabled by default so existing installs keep
# running the full suite after upgrading
DEFAULT_TESTS: Final = tuple(TEST_OPTIONS)

ATTRIBUTION: Final = "Data retrieved from Cloudflare Speed Test"
