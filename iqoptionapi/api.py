"""Module for IQ Option API."""

import time
import json
import logging
import threading
import requests
import ssl
from iqoptionapi.http.login import Login
from iqoptionapi.http.loginv2 import Loginv2
from iqoptionapi.http.getprofile import Getprofile
from iqoptionapi.http.auth import Auth
from iqoptionapi.http.token import Token
from iqoptionapi.http.appinit import Appinit
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
from iqoptionapi.ws.chanels.api_game_betinfo import Game_betinfo
from iqoptionapi.ws.chanels.instruments import Get_instruments
from iqoptionapi.ws.chanels.strike_list import Strike_list


from iqoptionapi.ws.chanels.traders_mood import Traders_mood_subscribe
from iqoptionapi.ws.chanels.traders_mood import Traders_mood_unsubscribe
from iqoptionapi.ws.chanels.buy_place_order_temp import Buy_place_order_temp
from iqoptionapi.ws.chanels.get_order import Get_order
from iqoptionapi.ws.chanels.get_positions import Get_positions
from iqoptionapi.ws.chanels.get_positions import Get_position
from iqoptionapi.ws.chanels.get_positions import Get_position_history
from iqoptionapi.ws.chanels.get_available_leverages import Get_available_leverages
from iqoptionapi.ws.chanels.cancel_order import Cancel_order
from iqoptionapi.ws.chanels.close_position import Close_position
from iqoptionapi.ws.chanels.get_overnight_fee import Get_overnight_fee
from iqoptionapi.ws.chanels.heartbeat import Heartbeat

from iqoptionapi.ws.chanels.subscribe import Subscribe_candles
from iqoptionapi.ws.chanels.unsubscribe import Unsubscribe_candles

from iqoptionapi.ws.chanels.subscribe import Subscribe_Instrument_Quites_Generated
from iqoptionapi.ws.chanels.unsubscribe import Unsubscribe_Instrument_Quites_Generated

from iqoptionapi.ws.chanels.api_game_getoptions import Getoptions
from iqoptionapi.ws.chanels.sell_option import Sell_Option
from iqoptionapi.ws.chanels.change_tpsl import Change_Tpsl

from iqoptionapi.ws.objects.timesync import TimeSync
from iqoptionapi.ws.objects.profile import Profile
from iqoptionapi.ws.objects.candles import Candles
from iqoptionapi.ws.objects.listinfodata import ListInfoData
from iqoptionapi.ws.objects.betinfo import Game_betinfo_data
import iqoptionapi.global_value as global_value
from collections import defaultdict

def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))

 

# InsecureRequestWarning: Unverified HTTPS request is being made.
# Adding certificate verification is strongly advised.
# See: https://urllib3.readthedocs.org/en/latest/security.html
requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member


class IQOptionAPI(object):  # pylint: disable=too-many-instance-attributes
    """Class for communication with IQ Option API."""
    # pylint: disable=too-many-public-methods

    timesync = TimeSync()
    profile = Profile()
    candles = Candles()
    listinfodata = ListInfoData()
    api_option_init_all_result = []
    
    #for digital
    position_changed=None
    instrument_quites_generated_data=nested_dict(2,dict)
    strike_list=None

    game_betinfo=Game_betinfo_data()
    instruments=None
    buy_id=None
    buy_order_id=None
    traders_mood={}#get hight(put) %
    order_data=None
    positions=None
    position=None
    position_history=None
    available_leverages=None
    order_canceled=None
    close_position_data=None
    overnight_fee=None
    #---for real time
    real_time_candles=nested_dict(3,dict)
    real_time_candles_maxdict_table=nested_dict(2,dict)
    candle_generated_check=nested_dict(2,dict)
    candle_generated_all_size_check=nested_dict(1,dict)
    #---for api_game_getoptions_result
    api_game_getoptions_result=None
    sold_options_respond=None
    tpsl_changed_respond=None
    #------------------
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
        #is used to determine if a buyOrder was set  or failed. If
        #it is None, there had been no buy order yet or just send.
        #If it is false, the last failed
        #If it is true, the last buy order was successful
        self.buy_successful = None


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
    def send_http_request_v2(self, url, method, data=None, params=None, headers=None): # pylint: disable=too-many-arguments
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
#------------------------------------------------------------------------
    @property
    def getprofile(self):
        """Property for get IQ Option http getprofile resource.

        :returns: The instance of :class:`Login
            <iqoptionapi.http.getprofile.Getprofile>`.
        """
        return Getprofile(self)
#for active code ...
    @property   
    def get_instruments(self):
        return Get_instruments(self)
#----------------------------------------------------------------------------     
    @property
    def ssid(self):
        """Property for get IQ Option websocket ssid chanel.

        :returns: The instance of :class:`Ssid
            <iqoptionapi.ws.chanels.ssid.Ssid>`.
        """
        return Ssid(self)
#--------------------------------------------------------------------------------
#trader mood 
    @property
    def subscribe_Traders_mood(self):
        return Traders_mood_subscribe(self)
    @property
    def unsubscribe_Traders_mood(self):
        return Traders_mood_unsubscribe(self)

#--------------------------------------------------------------------------------
#--------------------------subscribe&unsubscribe---------------------------------
#--------------------------------------------------------------------------------
    @property
    def subscribe(self):
        "candle-generated"
        """Property for get IQ Option websocket subscribe chanel.

        :returns: The instance of :class:`Subscribe
            <iqoptionapi.ws.chanels.subscribe.Subscribe>`.
        """
        return Subscribe(self)
    @property  
    def subscribe_all_size(self):
        return Subscribe_candles(self)

    @property
    def unsubscribe(self):
        """Property for get IQ Option websocket unsubscribe chanel.

        :returns: The instance of :class:`Unsubscribe
            <iqoptionapi.ws.chanels.unsubscribe.Unsubscribe>`.
        """
        return Unsubscribe(self)
    @property
    def unsubscribe_all_size(self):
        return Unsubscribe_candles(self)


#--------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
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
  
    def get_api_option_init_all(self):
        data = json.dumps(dict(name="api_option_init_all",
                               msg=""))
        self.websocket.send(data)
#-------------get information-------------   
    @property
    def get_betinfo(self):
        return Game_betinfo(self)
    @property
    def get_options(self):
        return Getoptions(self)

#____________for_______binary_______option_____________

    @property
    def buy(self):
        """Property for get IQ Option websocket buyv2 request.

        :returns: The instance of :class:`Buyv2
            <iqoptionapi.ws.chanels.buyv2.Buyv2>`.
        """
        self.buy_successful = None
        return Buyv2(self)
    
    @property
    def sell_option(self):
        return Sell_Option(self)
#____________________for_______digital____________________
    @property
    def get_strike_list(self):
        return Strike_list(self)
    @property
    def subscribe_instrument_quites_generated(self):
        return Subscribe_Instrument_Quites_Generated(self)
    @property
    def unsubscribe_instrument_quites_generated(self):
        return Unsubscribe_Instrument_Quites_Generated(self)



#____BUY_for__Forex__&&__stock(cfd)__&&__ctrpto_____
    @property
    def buy_order(self):
        return Buy_place_order_temp(self)
    @property
    def change_order(self):
        return Change_Tpsl(self)
    @property
    def get_order(self):
        return Get_order(self)
    @property
    def get_positions(self):
        return Get_positions(self)
    @property
    def get_position(self):
        return Get_position(self)
    @property
    def get_position_history(self):
        return Get_position_history(self)
    @property
    def get_available_leverages(self):
        return Get_available_leverages(self)
    @property
    def cancel_order(self):
        return Cancel_order(self)
    @property
    def close_position(self):
        return Close_position(self)
    @property
    def get_overnight_fee(self):
        return Get_overnight_fee(self)
#-------------------------------------------------------
    @property
    def heartbeat(self):
            return Heartbeat(self)
#-------------------------------------------------------
    def set_session_cookies(self):
        """Method to set session cookies."""
        cookies = dict(platform="15")
        self.session.headers["User-Agent"]="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
        requests.utils.add_dict_to_cookiejar(self.session.cookies, cookies)
       
    
    def connect(self):
        global_value.check_websocket_if_connect=None
        """Method for connection to IQ Option API."""
        response = self.login(self.username, self.password) # pylint: disable=not-callable
        ssid = response.cookies["ssid"]
        self.set_session_cookies()
        self.websocket_client = WebsocketClient(self)
 
        self.websocket_thread = threading.Thread(target=self.websocket.run_forever,kwargs={'sslopt':{"check_hostname": False, "cert_reqs": ssl.CERT_NONE, "ca_certs": "cacert.pem"}})                                                                #for fix pyinstall error: cafile, capath and cadata cannot be all omitted
        self.websocket_thread.daemon = True
        self.websocket_thread.start()
       
        while True:
            try:
                if global_value.check_websocket_if_connect==0 or global_value.check_websocket_if_connect==-1:
                    return False
                elif global_value.check_websocket_if_connect==1:
                    break
            except:
                pass

            pass

        self.ssid(ssid) # pylint: disable=not-callable
        self.timesync.server_timestamp=None
        while True:
            try:
                if self.timesync.server_timestamp!=None:
                    break
            except:
                pass
        return True
        
    def close(self):
        self.websocket.close()
        self.websocket_thread.join()

    def websocket_alive(self):
        return self.websocket_thread.is_alive()
    

