"""Module for IQ option websocket."""

import json
import logging
import websocket
import iqoptionapi.constants as OP_code
import iqoptionapi.global_value as global_value
class WebsocketClient(object):
    """Class for work with IQ option websocket."""

    def __init__(self, api):
        """
        :param api: The instance of :class:`IQOptionAPI
            <iqoptionapi.api.IQOptionAPI>`.
        """
        self.api = api
        self.wss = websocket.WebSocketApp(
            self.api.wss_url, on_message=self.on_message,
            on_error=self.on_error, on_close=self.on_close,
            on_open=self.on_open)

    def on_message(self, wss, message): # pylint: disable=unused-argument
        """Method to process websocket messages."""
        logger = logging.getLogger(__name__)
        logger.debug(message)

        message = json.loads(str(message))

        if message["name"] == "timeSync":
            self.api.timesync.server_timestamp = message["msg"]

        elif message["name"] == "profile":
            #--------------all-------------
            self.api.profile.msg=message["msg"]
            #---------------------------
            try:
                self.api.profile.balance = message["msg"]["balance"]
            except:
                pass
            
            try:
                self.api.profile.balance_id=message["msg"]["balance_id"]
            except:
                pass
            
            try:
                self.api.profile.balance_type=message["msg"]["balance_type"]
            except:
                pass

            try:
                self.api.profile.balances=message["msg"]["balances"]
            except:
                pass
        elif message["name"] == "candles":
            try:
                self.api.candles.candles_data = message["msg"]["candles"]
            except:
                pass
        #Make sure ""self.api.buySuccessful"" more stable
        #check buySuccessful have two fail action
        #if "user not authorized" we get buyV2_result !!!need to reconnect!!!
        #elif "we have user authoget_balancerized" we get buyComplete
        #I Suggest if you get selget_balancef.api.buy_successful==False you need to reconnect iqoption server
        elif message["name"] == "buyComplete":
            try:
                self.api.buy_successful = message["msg"]["isSuccessful"]
                self.api.buy_id= message["msg"]["result"]["id"]
            except:
                pass
        elif message["name"] == "buyV2_result":
            self.api.buy_successful = message["msg"]["isSuccessful"]
        #**********************************************************   
        elif message["name"] == "listInfoData":
           for get_m in message["msg"]:
               self.api.listinfodata.set(get_m["win"],get_m["game_state"],get_m["id"])

        elif message["name"] == "api_option_init_all_result":
            self.api.api_option_init_all_result = message["msg"]
        elif message["name"] == "candle-generated":
            Active_name=list(OP_code.ACTIVES.keys())[list(OP_code.ACTIVES.values()).index(message["msg"]["active_id"])]            
            self.api.real_time_candles[Active_name]= message["msg"]
        elif message["name"] == "instruments":
            self.api.instruments=message["msg"]
        
        elif message["name"]=="strike-list":
            try:
                time_key={}
                for i in message["msg"]["strike"]:
                    dd=i["call"]["id"].split("MC")
                    time_key[int(dd[1])/100000]=i["call"]["id"]
                expiration=message["msg"]["strike"][0]["call"]["id"].split("PT")[1].split("MC")[0]
                self.api.strike_list.put_All_data(message["msg"]["underlying"],expiration,time_key)
                #todo
            except:
                pass
    
    @staticmethod
    def on_error(wss, error): # pylint: disable=unused-argument
        """Method to process websocket errors."""
        logger = logging.getLogger(__name__)
        logger.error(error)
        global_value.check_websocket_if_connect=-1
    @staticmethod
    def on_open(wss): # pylint: disable=unused-argument
        """Method to process websocket open."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket client connected.")
        global_value.check_websocket_if_connect=1
    @staticmethod
    def on_close(wss): # pylint: disable=unused-argument
        """Method to process websocket close."""
        logger = logging.getLogger(__name__)
        logger.debug("Websocket connection closed.")
        global_value.check_websocket_if_connect=0
