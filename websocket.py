# -*- coding: utf-8 -*-
"""Module for IQ option websocket."""

import json
import logging
from datetime import datetime, timedelta
import time
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
        
        self.profile = None
        self.skey = None
        self.balance = None
        self.balance_id = None
        
        self.candles = []
        self.candles_new = False
        self.lasttimestamp = False
        self.nexttimestamp = False
        self.newMin = False

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
            self.name = self.message["name"]
            # return self.message

            if self.name == "newChartData":
                self.time = self.message["msg"]["time"]
                self.show_value = self.message["msg"]["show_value"]
                if self.lasttimestamp == False:
                    self.lasttimestamp = self.time - (self.time%60)
                    self.nexttimestamp = self.lasttimestamp + 60
                else:
                    time = datetime.fromtimestamp(self.time)
                    if time > datetime.fromtimestamp(self.lasttimestamp) + timedelta(seconds=61):
                        self.lasttimestamp = self.nexttimestamp
                        self.nexttimestamp = self.lasttimestamp + 60
                        self.newMin = True
                        
            if self.name == "profile":
                if self.profile == None:
                    if self.message["msg"] != False:
                        if 'balance' in self.message["msg"]:
                            self.balance = self.message["msg"]["balance"]
                        elif 'balance_id' in self.message["msg"]:
                            self.balance_id = self.message["msg"]["balance_id"]
                        elif 'skey' in self.message["msg"]:
                            self.skey = self.message["msg"]["skey"]
                            self.profile = True
                else:
                    if self.message["msg"] != False:
                        if self.balance_id != None:
                            if 'balance_id' in self.message["msg"]:
                                if self.message["msg"]["balance_id"] ==  self.balance_id:
                                    self.balance = self.message["msg"]["balance"]
                                    
                                    
                if self.name == 'candles':
                    if len(self.candles) == 0:
                        self.candles = self.message["msg"]["data"]
                        self.candles_count = 1
                    else:
                        for candle in self.message["msg"]["data"]:
                           self.candles.append(candle)
                        self.candles_count = self.candles_count + 1
                    self.candles_new = True


