# -*- coding: utf-8 -*-
"""Module for IQ option buy websocket chanel."""

from iqoption_api.chanel import Chanel


class Buy(Chanel):
    # pylint: disable=too-few-public-methods
    """Class for IQ option buy websocket chanel."""

    name = "buy"

    def __call__(self, time, show_value):
        """Method to send message to buy websocket chanel.

        :param msg: The websocket buy chanel message.
        """

        data = dict(price=10,
                    refund_value=0,
                    act=99,
                    exp=time + 60,
                    type="turbo",
                    direction="call",
                    value=show_value,
                    time=time)
                    # skey="27bcbe90b8b97401a447443433531495")

        self.send_wss_request(self.name, data)
