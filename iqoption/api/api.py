# -*- coding: utf-8 -*-
"""Module for IQ option api."""

import json
import threading

import requests

from iqoption.actives.setactives import SetActives
from iqoption.deals.buy import Buy
from iqoption.enums.directions import Direction
from iqoption.enums.strategies import Strategy
from iqoption.networking.websocket import Websocket
from iqoption.websocket.subscribe import Subscribe
from iqoption.websocket.unsubscribe import UnSubscribe
from ssid import Ssid

# InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised.
# See: https://urllib3.readthedocs.org/en/latest/security.html
requests.packages.urllib3.disable_warnings()


class IQOptionAPI(object):
    """Class for communication with IQ option api."""
    
    def __init__(self, ssid):
        """
        :param str ssid: Session Secure ID from Website
        """

        self.wss_url = "wss://iqoption.com/echo/websocket"
        self.websocket = None
        self.myssid = ssid

    def send_wss_request(self, name, msg):
        """
        Send wss request to IQ option server.
        :param name: Channel name
        :param msg Message

        :returns: 
        """
        data = json.dumps(dict(name=name, 
                               msg=msg))
        self.websocket.send(data)

    @property
    def ssid(self):
        """
        Property for get IQ option websocket ssid chanel.

        :returns: :class:`Ssid
            <iqoption_api.ssid.Ssid>`.
        """
        return Ssid(self)

    @property
    def subscribe(self):
        """
        Property for get IQ option websocket subscribe chanel.

        :returns: :class:`Subscribe
            <iqoption_api.subscribe.Subscribe>`.
        """
        return Subscribe(self)

    @property
    def unsubscribe(self):
        """
        Property for get IQ option websocket unsubscribe chanel.

        :returns: :class:`unsubscribe
            <iqoption_api.unsubscribe.UnSubscribe>`.
        """
        return UnSubscribe(self)

    @property
    def setactives(self):
        """
        Property for get IQ option websocket setactives chanel.

        :returns: :class:`setactives
            <iqoption_api.setactives.SetActives>`.
        """
        return SetActives(self)

    @property
    def buy(self):
        """
        Property for get IQ option websocket buy chanel.

        :returns: :class:`buy
            <iqoption_api.buy.Buy>`.
        """
        return Buy(self)

    def _thread(self):
        """Method for websocket thread.""" 
        self.websocket.run_forever()

    def connect(self, active, strategy, exp_period):
        """Method for connection to api."""

        websocket = Websocket(self.wss_url)
        websocket.connect()

        self.websocket = websocket
       
        websocket_thread = threading.Thread(target=self._thread)
        websocket_thread.daemon = True
        websocket_thread.start()

        self.ssid(self.myssid)

        self.subscribe("deposited")
        self.unsubscribe("deposited")
        self.unsubscribe("iqguard")
        self.unsubscribe("signal")
        self.unsubscribe("feedRecentBets")
        self.unsubscribe("feedRecentBets2")
        self.unsubscribe("feedTopTraders2")
        self.unsubscribe("feedRecentBetsMulti")
        self.unsubscribe("timeSync")
        self.setactives(active)

        ready_to_buy = True
        while True:
            if strategy == Strategy.candle_martin:
                activate_strategy(strategy)
                if ready_to_buy:
                    self.buy(active, Direction.call, exp_period, self.websocket.time)
                    ready_to_buy = False