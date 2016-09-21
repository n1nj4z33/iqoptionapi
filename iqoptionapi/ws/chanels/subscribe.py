"""Module for IQ option subscribe websocket chanel."""

from iqoptionapi.ws.chanels.base import Base


class Subscribe(Base):
    """Class for IQ option subscribe websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "subscribe"

    def __call__(self, chanel_name):
        """Method to send message to subscribe websocket chanel.

        :param chanel_name: The websocket chanel name to subsribe.
        """
        self.send_websocket_request(self.name, chanel_name)
