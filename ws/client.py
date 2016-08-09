# -*- coding: utf-8 -*-
"""Module for IQ option websocket."""

import json
import logging
import websocket


class WebsocketClient(object):
    """Class for work with IQ option websocket."""

    def __init__(self, api):
        """
        :param api: The instance of :class:`IQOptionAPI <iqapi.api.IQOptionAPI>`.
        """
        self.api = api
        self.wss = websocket.WebSocketApp(
            self.api.wss_url, on_message=self.on_message,
            on_error=self.on_error, on_close=self.on_close,
            on_open=self.on_open)

    def on_message(self, wss, message):
        """Method to process websocket messages."""
        # pylint: disable=unused-argument
        logger = logging.getLogger(__name__)
        logger.debug(message)

        message = json.loads(str(message))

        if message["name"] == "timeSync":
            self.api.timesync.server_timestamp = message["msg"]

        if message["name"] == "profile":
            self.api.profile.balance = message["msg"]["balance"]

        if message["name"] == "candles":
            self.api.candles.candles_data = message["msg"]["data"]

    @classmethod
    def on_error(cls, error):
        """Method to process websocket errors."""
        # pylint: disable=unused-argument
        logger = logging.getLogger(__name__)
        logger.error(error)

    @classmethod
    def on_open(cls):
        """Method to process websocket open."""
        # pylint: disable=unused-argument
        logger = logging.getLogger(__name__)
        logger.debug("Websocket client connected.")

    @classmethod
    def on_close(cls):
        """Method to process websocket close."""
        # pylint: disable=unused-argument
        logger = logging.getLogger(__name__)
        logger.debug("Websocket connection closed.")
