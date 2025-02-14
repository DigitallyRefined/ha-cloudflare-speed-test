"""Support for Cloudflare Speed Test internet speed testing sensor."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, cast

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import UnitOfDataRate, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    ATTR_BYTES_RECEIVED,
    ATTR_BYTES_SENT,
    ATTR_SERVER_COUNTRY,
    ATTR_SERVER_ID,
    ATTR_SERVER_NAME,
    ATTRIBUTION,
    DEFAULT_NAME,
    DOMAIN,
)
from .coordinator import CloudflareSpeedTestConfigEntry, CloudflareSpeedTestDataCoordinator


@dataclass(frozen=True)
class CloudflareSpeedTestSensorEntityDescription(SensorEntityDescription):
    """Class describing CloudflareSpeedTest sensor entities."""

    value: Callable = round


SENSOR_TYPES: tuple[CloudflareSpeedTestSensorEntityDescription, ...] = (
    CloudflareSpeedTestSensorEntityDescription(
        key="ping",
        translation_key="ping",
        name="Ping",
        native_unit_of_measurement=UnitOfTime.MILLISECONDS,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DURATION,
    ),
    CloudflareSpeedTestSensorEntityDescription(
        key="download",
        translation_key="download",
        name="Download",
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DATA_RATE,
        value=lambda value: round(value / 10**6, 2),
    ),
    CloudflareSpeedTestSensorEntityDescription(
        key="upload",
        translation_key="upload",
        name="Upload",
        native_unit_of_measurement=UnitOfDataRate.MEGABITS_PER_SECOND,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.DATA_RATE,
        value=lambda value: round(value / 10**6, 2),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: CloudflareSpeedTestConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Cloudflare_speed_test sensors."""
    cloudflarespeedtest_coordinator = config_entry.runtime_data
    async_add_entities(
        CloudflareSpeedTestSensor(cloudflarespeedtest_coordinator, description)
        for description in SENSOR_TYPES
    )


class CloudflareSpeedTestSensor(CoordinatorEntity[CloudflareSpeedTestDataCoordinator], SensorEntity):
    """Implementation of a Cloudflare Speed Test sensor."""

    entity_description: CloudflareSpeedTestSensorEntityDescription
    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: CloudflareSpeedTestDataCoordinator,
        description: CloudflareSpeedTestSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = description.key
        self._state: StateType = None
        self._attrs: dict[str, Any] = {}
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
            name=DEFAULT_NAME,
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def native_value(self) -> StateType:
        """Return native value for entity."""
        if self.coordinator.data:
            state = self.coordinator.data[self.entity_description.key]
            self._state = cast(StateType, self.entity_description.value(state))
        return self._state

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        if self.coordinator.data:
            self._attrs.update(
                {
                    ATTR_SERVER_NAME: self.coordinator.data["server"]["name"],
                    ATTR_SERVER_COUNTRY: self.coordinator.data["server"]["country"],
                    ATTR_SERVER_ID: self.coordinator.data["server"]["id"],
                }
            )

            if self.entity_description.key == "download":
                self._attrs[ATTR_BYTES_RECEIVED] = self.coordinator.data[
                    ATTR_BYTES_RECEIVED
                ]
            elif self.entity_description.key == "upload":
                self._attrs[ATTR_BYTES_SENT] = self.coordinator.data[ATTR_BYTES_SENT]

        return self._attrs
