# -*- coding: utf-8 -*-
"""Module for IQ option candles websocket chanel."""

from iqoption_api.ws.chanels.base import Base


class GetCandles(Base):
    """Class for IQ option candles websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "candles"

    def __call__(self, active, duration):
        """Method to send message to candles websocket chanel.

        :param msg: The websocket candles chanel message.
        """
        msg = {"active_id": active,
               "duration": duration,
               "chunk_size": 25,
               "from": self.api.timesync.server_timestamp - (duration * 2),
               "till": self.api.timesync.server_timestamp}

        self.send_websocket_request(self.name, msg)
