"""Module for IQ option unsubscribe websocket chanel."""

from iqoptionapi.ws.chanels.base import Base


class Unsubscribe(Base):
    """Class for IQ option unsubscribe websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "unSubscribe"

    def __call__(self, chanel_name):
        """Method to send message to unsubscribe websocket chanel.

        :param chanel_name: The websocket chanel name to unsubsribe.
        """
        self.send_websocket_request(self.name, chanel_name)
