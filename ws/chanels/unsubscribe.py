# -*- coding: utf-8 -*-
"""Module for IQ option unsubscribe websocket chanel."""

from iqoption_api.ws.chanels.base import Base


class Unsubscribe(Base):
    """Class for IQ option unsubscribe websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "unSubscribe"

    def __call__(self, msg):
        """Method to send message to unsubscribe websocket chanel.

        :param msg: The websocket unsubscribe chanel message.
        """
        self.send_websocket_request(self.name, msg)
