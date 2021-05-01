"""Threema Gateway notify component."""
import asyncio
import logging

import voluptuous as vol

from homeassistant.components.notify import (
  ATTR_DATA,
  PLATFORM_SCHEMA,
  BaseNotificationService,
)
import homeassistant.helpers.config_validation as cv

from .const import (
  CONF_SENDER_ID,
  CONF_SENDER_SECRET,
  CONF_ID_TYPE,
  CONF_RECP_ID,
)

""" Threema Imports """
from threema.gateway import (
  Connection,
  GatewayError,
  util,
)
from threema.gateway.simple import TextMessage

_LOGGER = logging.getLogger(__name__)

ATTR_FILENAMES = "attachments"

DEFAULT_TYPE = "basic"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
  {
    vol.Required(CONF_SENDER_ID): cv.string,
    vol.Required(CONF_SENDER_SECRET): cv.string,
    vol.Required(CONF_RECP_ID): vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_ID_TYPE, default=DEFAULT_TYPE): vol.In(["basic", "e2e"]),
  }
)

async def async_get_service(hass, config, discovery_info=None):
  """Get the Threema Gateway notification service."""

  sender_id = config[CONF_SENDER_ID]
  sender_secret = config[CONF_SENDER_SECRET]
  recp_ids = config[CONF_RECP_ID]

  return ThreemaNotificationService(sender_id, sender_secret, recp_ids)


class ThreemaNotificationService(BaseNotificationService):
  """Implement the notification service for Threema Gateway."""

  def __init__(self, sender_id, sender_secret, recp_ids):
    """Initialize the service."""

    self._sender_id = sender_id
    self._sender_secret = sender_secret
    self._recp_ids = recp_ids

  async def async_send_message(self, message="", **kwargs):
    """Send a message to a one or more recipients.
    """

    _LOGGER.debug("Sending Threema message")

    data = kwargs.get(ATTR_DATA)

    filenames = None
    if data is not None:
      if ATTR_FILENAMES in data:
        filenames = data[ATTR_FILENAMES]

    connection = Connection(
      identity=self._sender_id,
      secret=self._sender_secret,
      verify_fingerprint=True,
    )

    try:
      async with connection:
        for recp_id in self._recp_ids:
          message = TextMessage(
            connection=connection,
            to_id=recp_id,
            text=message
          )
          await message.send()
    except GatewayError as ex:
      _LOGGER.error("%s", ex)
      raise ex
