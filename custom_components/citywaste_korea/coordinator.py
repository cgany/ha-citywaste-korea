"""DataUpdateCoordinator for CityWaste Korea."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .citywaste_api import CityWasteApiError, CityWasteClient
from .const import (
    CONF_APTDONG,
    CONF_APTHONO,
    CONF_TAGPRINTCD,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(minutes=30)


class CityWasteCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to manage CityWaste API updates."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the coordinator."""

        data = {**entry.data, **entry.options}

        self.client = CityWasteClient(
            data[CONF_TAGPRINTCD],
            int(data[CONF_APTDONG]),
            int(data[CONF_APTHONO]),
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{entry.entry_id}",
            update_interval=UPDATE_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch the latest data from CityWaste."""

        try:
            return await self.hass.async_add_executor_job(
                self.client.fetch_month_data
            )
        except CityWasteApiError as err:
            raise UpdateFailed(str(err)) from err
