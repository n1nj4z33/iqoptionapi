"""Module for IQ Option API."""

import time
import json
import logging
import threading
import requests

from iqoptionapi.http.login import Login
from iqoptionapi.http.loginv2 import Loginv2
from iqoptionapi.http.getprofile import Getprofile
from iqoptionapi.http.auth import Auth
from iqoptionapi.http.token import Token
from iqoptionapi.http.appinit import Appinit
# from iqoptionapi.http.profile import Profile
from iqoptionapi.http.billing import Billing
from iqoptionapi.http.buyback import Buyback
from iqoptionapi.http.changebalance import Changebalance
from iqoptionapi.ws.client import WebsocketClient
from iqoptionapi.ws.chanels.ssid import Ssid
from iqoptionapi.ws.chanels.subscribe import Subscribe
from iqoptionapi.ws.chanels.unsubscribe import Unsubscribe
from iqoptionapi.ws.chanels.setactives import SetActives
from iqoptionapi.ws.chanels.candles import GetCandles
from iqoptionapi.ws.chanels.buyv2 import Buyv2

from iqoptionapi.ws.objects.timesync import TimeSync
from iqoptionapi.ws.objects.profile import Profile
from iqoptionapi.ws.objects.candles import Candles


# InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised.
# See: https://urllib3.readthedocs.org/en/latest/security.html
requests.packages.urllib3.disable_warnings()


class IQOptionAPI(object):
    """Class for communication with IQ Option API."""
    # pylint: disable=too-many-public-methods

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
            :class:`Resource <iqoptionapi.http.resource.Resource>`.

        :returns: The full url to IQ Option http resource.
        """
        return "/".join((self.https_url, resource.url))

    def send_http_request(self, resource, method, data=None, params=None, headers=None): # pylint: disable=too-many-arguments
        """Send http request to IQ Option server.

        :param resource: The instance of
            :class:`Resource <iqoptionapi.http.resource.Resource>`.
        :param str method: The http request method.
        :param dict data: (optional) The http request data.
        :param dict params: (optional) The http request params.
        :param dict headers: (optional) The http request headers.

        :returns: The instance of :class:`Response <requests.Response>`.
        """
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

        :returns: The instance of :class:`Login
            <iqoptionapi.http.login.Login>`.
        """
        return Login(self)

    @property
    def loginv2(self):
        """Property for get IQ Option http loginv2 resource.

        :returns: The instance of :class:`Loginv2
            <iqoptionapi.http.loginv2.Loginv2>`.
        """
        return Loginv2(self)

    @property
    def auth(self):
        """Property for get IQ Option http auth resource.

        :returns: The instance of :class:`Auth
            <iqoptionapi.http.auth.Auth>`.
        """
        return Auth(self)

    @property
    def appinit(self):
        """Property for get IQ Option http appinit resource.

        :returns: The instance of :class:`Appinit
            <iqoptionapi.http.appinit.Appinit>`.
        """
        return Appinit(self)

    @property
    def token(self):
        """Property for get IQ Option http token resource.

        :returns: The instance of :class:`Token
            <iqoptionapi.http.auth.Token>`.
        """
        return Token(self)

    # @property
    # def profile(self):
    #     """Property for get IQ Option http profile resource.

    #     :returns: The instance of :class:`Profile
    #         <iqoptionapi.http.profile.Profile>`.
    #     """
    #     return Profile(self)

    @property
    def changebalance(self):
        """Property for get IQ Option http changebalance resource.

        :returns: The instance of :class:`Changebalance
            <iqoptionapi.http.changebalance.Changebalance>`.
        """
        return Changebalance(self)

    @property
    def billing(self):
        """Property for get IQ Option http billing resource.

        :returns: The instance of :class:`Billing
            <iqoptionapi.http.billing.Billing>`.
        """
        return Billing(self)

    @property
    def buyback(self):
        """Property for get IQ Option http buyback resource.

        :returns: The instance of :class:`Buyback
            <iqoptionapi.http.buyback.Buyback>`.
        """
        return Buyback(self)

    @property
    def getprofile(self):
        """Property for get IQ Option http getprofile resource.

        :returns: The instance of :class:`Login
            <iqoptionapi.http.getprofile.Getprofile>`.
        """
        return Getprofile(self)

    @property
    def ssid(self):
        """Property for get IQ Option websocket ssid chanel.

        :returns: The instance of :class:`Ssid
            <iqoptionapi.ws.chanels.ssid.Ssid>`.
        """
        return Ssid(self)

    @property
    def subscribe(self):
        """Property for get IQ Option websocket subscribe chanel.

        :returns: The instance of :class:`Subscribe
            <iqoptionapi.ws.chanels.subscribe.Subscribe>`.
        """
        return Subscribe(self)

    @property
    def unsubscribe(self):
        """Property for get IQ Option websocket unsubscribe chanel.

        :returns: The instance of :class:`Unsubscribe
            <iqoptionapi.ws.chanels.unsubscribe.Unsubscribe>`.
        """
        return Unsubscribe(self)

    @property
    def setactives(self):
        """Property for get IQ Option websocket setactives chanel.

        :returns: The instance of :class:`SetActives
            <iqoptionapi.ws.chanels.setactives.SetActives>`.
        """
        return SetActives(self)

    @property
    def getcandles(self):
        """Property for get IQ Option websocket candles chanel.

        :returns: The instance of :class:`GetCandles
            <iqoptionapi.ws.chanels.candles.GetCandles>`.
        """
        return GetCandles(self)

    @property
    def buy(self):
        """Property for get IQ Option websocket buyv2 request.

        :returns: The instance of :class:`Buyv2
            <iqoptionapi.ws.chanels.buyv2.Buyv2>`.
        """
        return Buyv2(self)

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
