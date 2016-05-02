# -*- coding: utf-8 -*-
"""Module for IQ option unsubscribe websocket chanel."""

from iqoption.networking.chanel import Chanel


class UnSubscribe(Chanel):
    # pylint: disable=too-few-public-methods
    """Class for IQ option unsubscribe websocket chanel."""

    name = "unSubscribe"

    def __call__(self, msg):
        """Method to send message to unsubscribe websocket chanel.

        :param msg: The websocket unsubscribe chanel message.
        """
        self.send_wss_request(self.name, msg)
