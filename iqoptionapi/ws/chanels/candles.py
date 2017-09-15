"""Module for IQ option candles websocket chanel."""

from iqoptionapi.ws.chanels.base import Base


class GetCandles(Base):
    """Class for IQ option candles websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "candles"

    def __call__(self, active_id, duration, amount):
        """Method to send message to candles websocket chanel.

        :param active_id: The active/asset identifier.
        :param duration: The candle duration (timeframe for the candles).
        :param amount: The number of candles you want to have
        """
        data = {"active_id": active_id,
                "duration": duration,
                "chunk_size": 25,
                "from": self.api.timesync.server_timestamp - (duration * amount),
                "till": self.api.timesync.server_timestamp}

        self.send_websocket_request(self.name, data)
