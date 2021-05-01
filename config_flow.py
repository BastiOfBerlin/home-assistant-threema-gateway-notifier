import logging
from homeassistant import config_entries, exceptions

import voluptuous as vol

from .const import (
  DOMAIN,
  CONF_SENDER_ID,
  CONF_SENDER_SECRET,
  CONF_ID_TYPE,
  CONF_RECP_ID,
)

DEFAULT_TYPE = "basic"

DATA_SCHEMA = vol.Schema(
  {
    vol.Required(CONF_SENDER_ID): str,
    vol.Required(CONF_SENDER_SECRET): str,
    vol.Required(CONF_RECP_ID): str,
    vol.Optional(CONF_ID_TYPE, default=DEFAULT_TYPE): vol.In(["basic", "e2e"]),
  }
)

_LOGGER = logging.getLogger(__name__)

async def validate_input(data: dict):
  if len(data[CONF_SENDER_ID]) != 8:
    raise InvalidSenderId
  # TODO: more validation

class ThreemaGatewayConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
  VERSION = 1
  CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_PUSH 

  async def async_step_user(self, user_input=None):
    """Handle the initial step."""
    errors = {}
    if user_input is not None:
      try:
        await validate_input(user_input)
        return self.async_create_entry(
          title = user_input[CONF_SENDER_ID],
          data = {
            CONF_SENDER_ID: user_input[CONF_SENDER_ID],
            CONF_SENDER_SECRET: user_input[CONF_SENDER_SECRET],
            CONF_ID_TYPE: user_input[CONF_ID_TYPE],
            CONF_RECP_ID: user_input[CONF_RECP_ID],
          },
        )
      except InvalidSenderId:
        errors[CONF_SENDER_ID] = "invalid_sender_id"
      except Exception as ex:  # pylint: disable=broad-except
        _LOGGER.exception("Unexpected exception")
        errors["base"] = "unknown"

    return self.async_show_form(
      step_id="user", data_schema=DATA_SCHEMA, errors=errors
    )

class InvalidSenderId(exceptions.HomeAssistantError):
    """Error to indicate an invalid sender id."""
