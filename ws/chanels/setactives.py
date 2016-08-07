# -*- coding: utf-8 -*-
"""Module for IQ option setactives websocket chanel."""

from iqoption_api.ws.chanels.base import Base


class SetActives(Base):
    """Class for IQ option setactives websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "setActives"

    def __call__(self, actives):
        """Method to send message to setactives websocket chanel.

        :param msg: The websocket setactives chanel message.
        """
        msg = dict(actives=actives)
        self.send_websocket_request(self.name, msg)
