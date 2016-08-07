# -*- coding: utf-8 -*-
"""Module for IQ option API ssid websocket chanel."""

from iqoption_api.ws.chanels.base import Base


class Ssid(Base):
    """Class for IQ option API ssid websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "ssid"

    def __call__(self, msg):
        """Method to send message to ssid websocket chanel.

        :param msg: The websocket ssid chanel message.
        """
        self.send_websocket_request(self.name, msg)
