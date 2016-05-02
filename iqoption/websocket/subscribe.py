# -*- coding: utf-8 -*-
"""Module for IQ option subscribe websocket chanel."""

from iqoption.networking.chanel import Chanel


class Subscribe(Chanel):
    # pylint: disable=too-few-public-methods
    """Class for IQ option subscribe websocket chanel."""

    name = "subscribe"

    def __call__(self, msg):
        """Method to send message to subscribe websocket chanel.

        :param msg: The websocket subscribe chanel message.
        """
        self.send_wss_request(self.name, msg)
