# -*- coding: utf-8 -*-
"""Module for IQ option subscribe websocket chanel."""

from iqoption_api.ws.chanels.base import Base


class Subscribe(Base):
    """Class for IQ option subscribe websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "subscribe"

    def __call__(self, msg):
        """Method to send message to subscribe websocket chanel.

        :param msg: The websocket subscribe chanel message.
        """
        self.send_websocket_request(self.name, msg)
