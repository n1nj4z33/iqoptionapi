# -*- coding: utf-8 -*-
"""Module for IQ option setactives websocket chanel."""

from iqoption.networking.chanel import Chanel


class SetActives(Chanel):
    # pylint: disable=too-few-public-methods
    """Class for IQ option setactives websocket chanel."""

    name = "setActives"

    def __call__(self, msg):
        """Method to send message to setactives websocket chanel.

        :param msg: The websocket setactives chanel message.
        """
        self.send_wss_request(self.name, {"actives": [msg]})
