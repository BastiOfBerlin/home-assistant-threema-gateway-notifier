""" Config class"""
from .const import (
  CONF_RECP_ID,
)

def parseRecipients(inp):
  s = inp.strip()
  if len(s) == 0:
    return []
  return list(map(lambda s: s.strip(), s.split(",")))

class Conf:
  def __init__(self, sender_id, sender_secret, gateway_mode, **kwargs):
    self._gateway_mode = gateway_mode
    self._sender_id = sender_id
    self._sender_secret = sender_secret
    self._recp_ids = parseRecipients(kwargs.get(CONF_RECP_ID, ""))

  @property
  def sender_id(self):
    return self._sender_id

  @property
  def sender_secret(self):
    return self._sender_secret

  @property
  def recp_ids(self):
    return self._recp_ids
