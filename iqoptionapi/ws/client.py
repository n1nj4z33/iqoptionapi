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
    def dict_queue_add(self,dict,maxdict,key1,key2,key3,value):
        if key3 in dict[key1][key2]:
                    dict[key1][key2][key3]=value
        else:
            while True:
                try:
                    dic_size=len(dict[key1][key2])
                except:
                    dic_size=0
                if dic_size<maxdict:
                    dict[key1][key2][key3]=value
                    break
                else:
                    #del mini key
                    del dict[key1][key2][sorted(dict[key1][key2].keys(), reverse=False)[0]]   
    def on_message(self, wss, message): # pylint: disable=unused-argument
        """Method to process websocket messages."""
        logger = logging.getLogger(__name__)
        logger.debug(message)

        message = json.loads(str(message))

        if message["name"] == "timeSync":
            self.api.timesync.server_timestamp = message["msg"]
        elif message["name"] =="heartbeat":
            try:
                self.api.heartbeat(message["msg"])
            except:
                pass
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
        #######################################################
        #---------------------for_realtime_candle______________
        #######################################################
        elif message["name"] == "candle-generated":
            Active_name=list(OP_code.ACTIVES.keys())[list(OP_code.ACTIVES.values()).index(message["msg"]["active_id"])]            
            
            active=str(Active_name)
            size=int(message["msg"]["size"])
            from_=int(message["msg"]["from"])
            msg=message["msg"]
            maxdict=self.api.real_time_candles_maxdict_table[Active_name][size]

            self.dict_queue_add(self.api.real_time_candles,maxdict,active,size,from_,msg)
            self.api.candle_generated_check[active][size]=True
            

        elif message["name"] == "candles-generated":
            Active_name=list(OP_code.ACTIVES.keys())[list(OP_code.ACTIVES.values()).index(message["msg"]["active_id"])] 
            active=str(Active_name)      
            for k,v in message["msg"]["candles"].items():
                v["active_id"]=message["msg"]["active_id"]
                v["at"]=message["msg"]["at"]
                v["ask"]=message["msg"]["ask"]
                v["bid"]=message["msg"]["bid"]
                v["close"]=message["msg"]["value"]
                v["size"]=int(k)
                size=int(v["size"])
                from_=int(v["from"])
                maxdict=self.api.real_time_candles_maxdict_table[Active_name][size]
                msg=v
                self.dict_queue_add(self.api.real_time_candles,maxdict,active,size,from_,msg)
            self.api.candle_generated_all_size_check[active]=True 
                
        #######################################################
        #______________________________________________________
        #######################################################
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

        elif message["name"]=="api_game_betinfo_result":
            try:
                self.api.game_betinfo.isSuccessful=message["msg"]["isSuccessful"]
                self.api.game_betinfo.dict=message["msg"]
            except:
                pass
        elif message["name"]=="traders-mood-changed":
            self.api.traders_mood[message["msg"]["asset_id"]]=message["msg"]["value"]
        #------for forex&cfd&crypto..
        elif message["name"]=="order-placed-temp":
            self.api.buy_order_id= message["msg"]["id"]
        elif message["name"]=="order":
            self.api.order_data=message
        elif message["name"]=="positions":
            self.api.positions=message
        elif message["name"]=="position-history":
            self.api.position_history=message
        elif message["name"]=="available-leverages":
            self.api.available_leverages=message
        elif message["name"]=="order-canceled":
            self.api.order_canceled=message
        elif message["name"]=="position-closed":
            self.api.close_position_data=message
        elif message["name"]=="overnight-fee":
            self.api.overnight_fee=message
        elif message["name"]=="api_game_getoptions_result":
            self.api.api_game_getoptions_result=message
        elif message["name"]=="sold-options":
            self.api.sold_options_respond=message

    
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
