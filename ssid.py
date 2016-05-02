# -*- coding: utf-8 -*-
"""Module for IQ option ssid websocket chanel."""

from iqoption_api.chanel import Chanel


class Ssid(Chanel):
    # pylint: disable=too-few-public-methods
    """Class for IQ option ssid websocket chanel."""

    name = "ssid"

    def __call__(self, msg):
        """Method to send message to ssid websocket chanel.

        :param msg: The websocket ssid chanel message.
        """
        self.send_wss_request(self.name, msg)
