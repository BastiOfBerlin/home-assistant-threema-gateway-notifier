"""The Threema Gateway component."""
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from . import conf
from .const import (
  DOMAIN,
  CONF_SENDER_ID,
  CONF_SENDER_SECRET,
  CONF_ID_TYPE,
  CONF_RECP_ID,
)

PLATFORMS = ["sensor"]

async def async_setup(hass: HomeAssistant, config: dict):
  hass.data.setdefault(DOMAIN, {})
  return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
  """Set up from a config entry."""
  # Store config
  hass.data[DOMAIN][entry.entry_id] = conf.Conf(entry.data[CONF_SENDER_ID], entry.data[CONF_SENDER_SECRET], entry.data[CONF_ID_TYPE], CONF_RECP_ID=entry.data[CONF_RECP_ID])

  for component in PLATFORMS:
    hass.async_create_task(
      hass.config_entries.async_forward_entry_setup(entry, component)
    )

  return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
  """Unload a config entry."""
  unload_ok = all(
    await asyncio.gather(
      *[
        hass.config_entries.async_forward_entry_unload(entry, component)
        for component in PLATFORMS
      ]
    )
  )
  if unload_ok:
    hass.data[DOMAIN].pop(entry.entry_id)

  return unload_ok
