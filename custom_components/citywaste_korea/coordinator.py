"""DataUpdateCoordinator for CityWaste Korea."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .citywaste_api import CityWasteApiError

_LOGGER = logging.getLogger(__name__)


class CityWasteCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinate CityWaste data updates."""

    def __init__(
        self,
        hass: HomeAssistant,
        client,
    ) -> None:
        """Initialize coordinator."""
        self.client = client

        super().__init__(
            hass,
            _LOGGER,
            name="CityWaste Korea",
            update_interval=timedelta(minutes=30),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from CityWaste Korea."""
        try:
            return await self.hass.async_add_executor_job(
                self.client.fetch_month_data
            )
        except CityWasteApiError as err:
            raise UpdateFailed(str(err)) from err
