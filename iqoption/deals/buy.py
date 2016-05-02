# -*- coding: utf-8 -*-
"""Module for IQ option buy websocket chanel."""

from iqoption.networking.chanel import Chanel


class Buy(Chanel):
    # pylint: disable=too-few-public-methods
    """Class for IQ option buy websocket chanel."""

    name = "buy"

    def __call__(self, active, direction, exp_period, time):
        """Method to send message to buy websocket chanel.

        :param msg: The websocket buy chanel message.
        """

        data = dict(price=10,
                    act=active,
                    exp=time + exp_period * 60,
                    type="turbo",
                    direction=direction,
                    time=time)

        self.send_wss_request(self.name, data)
