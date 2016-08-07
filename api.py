# -*- coding: utf-8 -*-
"""Module for IQ Option API."""

import time
import json
import logging
import threading
import requests

from iqoption_api.http.login import Login
from iqoption_api.http.getprofile import Getprofile
from iqoption_api.ws.client import WebsocketClient
from iqoption_api.ws.chanels.ssid import Ssid
from iqoption_api.ws.chanels.subscribe import Subscribe
from iqoption_api.ws.chanels.unsubscribe import Unsubscribe
from iqoption_api.ws.chanels.setactives import SetActives
from iqoption_api.ws.chanels.candles import GetCandles
from iqoption_api.ws.chanels.buy import Buy

from iqoption_api.ws.objects.timesync import TimeSync
from iqoption_api.ws.objects.profile import Profile
from iqoption_api.ws.objects.candles import Candles


# InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised.
# See: https://urllib3.readthedocs.org/en/latest/security.html
requests.packages.urllib3.disable_warnings()


class IQOptionAPI(object):
    """Class for communication with IQ Option API."""

    timesync = TimeSync()
    profile = Profile()
    candles = Candles()

    def __init__(self, host, username, password, proxies=None):
        """
        :param str host: The hostname or ip address of a IQ Option server.
        :param str username: The username of a IQ Option server.
        :param str password: The password of a IQ Option server.
        :param dict proxies: (optional) The http request proxies.
        """
        self.https_url = "https://{host}/api".format(host=host)
        self.wss_url = "wss://{host}/echo/websocket".format(host=host)
        self.websocket_client = None
        self.session = requests.Session()
        self.session.verify = False
        self.session.trust_env = False
        self.username = username
        self.password = password
        self.proxies = proxies

    def prepare_http_url(self, resource):
        """Construct http url from resource url.

        :param resource: The instance of
            :class:`Resource <iqoption_api.http.resource.Resource>`.

        :returns: The full url to IQ Option http resource.
        """
        return '/'.join((self.https_url, resource.url))

    def send_http_request(self, resource, method, data=None, params=None, headers=None):
        """Send http request to IQ Option server.

        :param resource: The instance of
            :class:`Resource <iqoption_api.http.resource.Resource>`.
        :param str method: The http request method.
        :param dict data: (optional) The http request data.
        :param dict params: (optional) The http request params.
        :param dict headers: (optional) The http request headers.

        :returns: The instance of :class:`Response <requests.Response>`.
        """
        # pylint: disable=too-many-arguments
        logger = logging.getLogger(__name__)
        url = self.prepare_http_url(resource)

        logger.debug(url)

        response = self.session.request(method=method,
                                        url=url,
                                        data=data,
                                        params=params,
                                        headers=headers,
                                        proxies=self.proxies)
        logger.debug(response)
        logger.debug(response.text)
        logger.debug(response.headers)
        logger.debug(response.cookies)

        response.raise_for_status()
        return response

    @property
    def websocket(self):
        """Property to get websocket.

        :returns: The instance of :class:`WebSocket <websocket.WebSocket>`.
        """
        return self.websocket_client.wss

    def send_websocket_request(self, name, msg):
        """Send websocket request to IQ Option server.

        :param str name: The websocket request name.
        :param dict msg: The websocket request msg.
        """
        logger = logging.getLogger(__name__)

        data = json.dumps(dict(name=name,
                               msg=msg))
        logger.debug(data)
        self.websocket.send(data)

    @property
    def login(self):
        """Property for get IQ Option http login resource.

        :returns: The instance of
            :class:`Login <iqoption_api.http.login.Login>`.
        """
        return Login(self)

    @property
    def getprofile(self):
        """Property for get IQ Option http getprofile resource.

        :returns: The instance of
            :class:`Login <iqoption_api.http.getprofile.Getprofile>`.
        """
        return Getprofile(self)

    @property
    def ssid(self):
        """Property for get IQ Option websocket ssid chanel.

        :returns: The instance of :class:`Ssid <iqoption_api.ws.chanels.ssid.Ssid>`.
        """
        return Ssid(self)

    @property
    def subscribe(self):
        """Property for get IQ Option websocket subscribe chanel.

        :returns: The instance of
            :class:`Subscribe <iqoption_api.ws.chanels.subscribe.Subscribe>`.
        """
        return Subscribe(self)

    @property
    def unsubscribe(self):
        """Property for get IQ Option websocket unsubscribe chanel.

        :returns: The instance of
            :class:`Unsubscribe <iqoption_api.ws.chanels.unsubscribe.Unsubscribe>`.
        """
        return Unsubscribe(self)

    @property
    def setactives(self):
        """Property for get IQ Option websocket setactives chanel.

        :returns: The instance of
            :class:`SetActives <iqoption_api.ws.chanels.setactives.SetActives>`.
        """
        return SetActives(self)

    @property
    def getcandles(self):
        """Property for get IQ Option websocket candles chanel.

        :returns: The instance of
            :class:`GetCandles <iqoption_api.ws.chanels.candles.GetCandles>`.
        """
        return GetCandles(self)

    @property
    def buy(self):
        """Property for get IQ Option websocket buy request.

        :returns: The instance of :class:`Buy <iqoption_api.ws.chanels.buy.Buy>`.
        """
        return Buy(self)

    def set_session_cookies(self):
        """Method to set session cookies."""
        cookies = dict(platform="9")
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies)
        self.getprofile() # pylint: disable=not-callable

    def connect(self):
        """Method for connection to IQ Option API."""
        response = self.login(self.username, self.password) # pylint: disable=not-callable
        ssid = response.cookies["ssid"]
        self.set_session_cookies()
        self.websocket_client = WebsocketClient(self)

        websocket_thread = threading.Thread(target=self.websocket.run_forever)
        websocket_thread.daemon = True
        websocket_thread.start()

        time.sleep(5)

        self.ssid(ssid) # pylint: disable=not-callable
