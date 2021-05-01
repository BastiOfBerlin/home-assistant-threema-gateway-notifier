"""Platform for THreema credit sensor integration."""
from homeassistant.helpers.entity import Entity

import asyncio
import logging

from .const import DOMAIN

""" Threema Imports """
from threema.gateway import (
  Connection,
  GatewayError,
  util,
)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_devices):
  conf = hass.data[DOMAIN][config_entry.entry_id]
  async_add_devices([ThreemaCreditsSensor(conf)])


class ThreemaCreditsSensor(Entity):

  def __init__(self, conf):
    """Initialize the sensor."""
    self._credits = None
    self._conf = conf

  @property
  def name(self):
    """Return the name of the sensor."""
    return 'Threema Remaining Credits'

  @property
  def should_poll(self):
    """We need to be polled."""
    return True

  @property
  def state(self):
    """Return the state of the sensor."""
    return self._credits

  async def async_update(self):
    """Fetch new state from Gateway."""
    _LOGGER.debug("Fetching Threema Cedits")
    connection = Connection(
      identity=self._conf.sender_id,
      secret=self._conf.sender_secret,
      verify_fingerprint=True,
    )
    try:
      async with connection:
        self._credits = await connection.get_credits()
    except GatewayError as ex:
      _LOGGER.error("Threema Gateway error: %s", ex)
      raise ex
