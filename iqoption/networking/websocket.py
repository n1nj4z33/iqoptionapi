# -*- coding: utf-8 -*-
"""Module for IQ option websocket."""

import json
import logging
from ws4py.client.threadedclient import WebSocketClient


class Websocket(WebSocketClient):
    """Class for work with IQ option websocket."""
    
    def __init__(self, url, protocols=None, extensions=None,
                 heartbeat_freq=None, ssl_options=None, headers=None):
        # pylint: disable=too-many-arguments
        super(Websocket, self).__init__(url, protocols, extensions,
                                        heartbeat_freq, ssl_options, headers)
        self.message = None
        self.time = None
        self.show_value = None

    def received_message(self, message):
        """
        Catch all incoming websocket messages.

        :param str message: Incoming websocket message.

        :returns: Incoming message, converted to json or None.
        """
        logger = logging.getLogger(__name__)
        logger.debug(message)
        if message:
            self.message = json.loads(str(message))
            # return self.message

            if self.message["name"] == "timeSync":
                self.time = self.message["msg"]
                #self.show_value = self.message["msg"]["show_value"]


