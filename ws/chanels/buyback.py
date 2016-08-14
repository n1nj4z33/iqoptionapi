# -*- coding: utf-8 -*-
"""Module for IQ Option buyback websocket chanel."""

from .base import Base


class Buyback(Base):
    """Class for IQ option subscribe to buyback websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "buyback"

    def __call__(self):
        """Method to send message to buyback websocket chanel."""
        pass
