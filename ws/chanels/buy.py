# -*- coding: utf-8 -*-
"""Module for IQ Option buy websocket chanel."""

from iqoption_api.ws.chanels.base import Base


class Buy(Base):
    """Class for IQ option buy websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "buyV2"

    def __call__(self, signal):
        """Method to send message to buy websocket chanel.

        :param msg: The websocket buy chanel message.
        """
        msg = dict(price=signal.price,
                   act=signal.active,
                   exp=self.api.timesync.expiration_timestamp,
                   type=signal.option,
                   direction=signal.direction,
                   time=self.api.timesync.server_timestamp
                  )

        self.send_websocket_request(self.name, msg)
