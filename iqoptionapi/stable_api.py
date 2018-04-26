#python
from iqoptionapi.api import IQOptionAPI
import iqoptionapi.constants as OP_code
import threading
import time
import numpy as np
import logging

class IQ_Option:
    def __init__(self,email,password):
        self.email=email
        self.password=password
        self.suspend = 0.6
        self.connect()
        self.thread_collect_realtime={}
        
    def connect(self):
        while True:
            try:
                self.api = IQOptionAPI("iqoption.com", self.email, self.password)
                self.api.connect()
                time.sleep(self.suspend)
                break
            except:
                logging.error('fail connect()')
                pass
    def get_all_init(self):
        self.api.api_option_init_all_result = None
        self.api.get_api_option_init_all()
        while self.api.api_option_init_all_result == None:
            pass
        return self.api.api_option_init_all_result
    def get_profit(self,ACTIVES):
        init_info=self.get_all_init()
        return (100.0-init_info["result"]["turbo"]["actives"][str(OP_code.ACTIVES[ACTIVES])]["option"]["profit"]["commission"])/100.0
    def get_all_profit(self):
        all_profit={}
        init_info = self.get_all_init()
        for active in OP_code.ACTIVES:
            try:
                prof = (100.0-init_info["result"]["turbo"]["actives"][str(OP_code.ACTIVES[active])]["option"]["profit"]["commission"])/100.0
                all_profit[active]=prof
            except:
                pass
        return all_profit
    def get_balance(self):
        while True:
            try:
                return self.api.profile.balance
            except:
                logging.error('fail get_balance()')
                pass
    def change_balance(self,Balance_MODE):
        real_id=None
        practice_id=None
        for accunt in self.api.balances:
            if accunt["type"]==1:
                real_id=accunt["id"]
            if accunt["type"]==4:
                practice_id=accunt["id"]
        while self.get_balance_mode()!=Balance_MODE:
            if Balance_MODE=="REAL":
                self.api.changebalance(real_id)
            elif Balance_MODE=="PRACTICE":
                self.api.changebalance(practice_id)
            else:
                print("ERROR doesn't have this mode")
                exit(1)
 #######################**********candles***********#######################
    def get_candles(self,ACTIVES,interval,count,endtime):
        while True:
            try:
                self.api.getcandles(OP_code.ACTIVES[ACTIVES], interval,count,endtime)
                break
            except:
                logging.error('fail get_candles need reconnect')
                self.connect()
                pass
        while self.api.candles.candles_data==None:
            pass
        return self.api.candles.candles_data
################################################################################
###################             real time            ###########################    
################################################################################
                    #all
    def start_all_candles_stream(self):
        while self.api.real_time_candles == {}:
            for ACTIVES_name in OP_code.ACTIVES:
                self.api.subscribe_candle(OP_code.ACTIVES[ACTIVES_name])
    def get_all_realtime_candles(self):
        return self.api.real_time_candles
    def stop_all_candles_stream(self):
        while self.api.real_time_candles != {}:
            self.api.real_time_candles = {}
            time.sleep(1)
            for ACTIVES_name in OP_code.ACTIVES:
                self.api.unsubscribe_candle(OP_code.ACTIVES[ACTIVES_name])
    
                    ##one
    def start_candles_stream(self,ACTIVES):
        while self.api.real_time_candles == {}:
            self.api.subscribe_candle(OP_code.ACTIVES[ACTIVES])

    def get_realtime_candles(self,ACTIVES):
        while True:
            try:
                return self.api.real_time_candles[ACTIVES]
            except:
                pass
    def stop_candles_stream(self,ACTIVES):
        while self.api.real_time_candles != {}:
            self.api.real_time_candles = {}
            time.sleep(3)
            self.api.unsubscribe_candle(OP_code.ACTIVES[ACTIVES])
###################################collect realtime###################################
                #####dict controler####
    def dict_queue_add(self,dict,maxdict,key,value):
        while True:
            if len(dict)<maxdict:
                dict[key]=value
                break
            else:
                #del mini key
                del dict[sorted(dict.keys(), reverse=False)[0]]



    def thread_realtime(self,ACTIVES,maxdict):
        t = threading.currentThread()
        while getattr(t,"do_run",True):
            candles=self.get_realtime_candles(ACTIVES)
            self.dict_queue_add(self.thread_collect_realtime,maxdict,candles["at"],candles)
        self.thread_collect_realtime={}

    def collect_realtime_candles_thread_start(self,ACTIVES,maxdict):
        t = threading.Thread(target=self.thread_realtime, args=(ACTIVES,maxdict))
        t.start()
        return t
    def collect_realtime_candles_thread_stop(self,thread): 
        thread.do_run = False
        thread.join() 



    def collect_realtime_candles(self,ACTIVES,collect_time):
        #doing while untill time stop
        collect={}
        start=time.time()
        while time.time()<start+collect_time:
            candles=self.get_realtime_candles(ACTIVES) 
            collect[candles["at"]]=candles
        return collect
    

##############################################################################################
    def get_candles_as_array(self,ACTIVES,interval,count,endtime):
        candles=self.get_candles(ACTIVES,interval,count,endtime)
        ans = np.empty(shape=(len(candles), 4))
        for idx, candle in enumerate(candles):
            ans[idx][0] = candle["open"]
            ans[idx][1] = candle["close"]
            ans[idx][2] = candle["min"]
            ans[idx][3] = candle["max"]
        return ans

    def get_balance_mode(self):
        time.sleep(self.suspend)
        if self.api.balance_type==1:
            return "REAL"
        elif self.api.balance_type==4:
            return "PRACTICE"
    def check_win(self):
        #'win'：win money 'equal'：no win no loose   'loose':loose money
        self.api.listinfodata.__init__()
        while True:
            try:
                state=self.api.listinfodata.current_listinfodata.game_state
                if state==1:
                    break
            except:
                #print("connect error")
                pass
        return self.api.listinfodata.current_listinfodata.win
    def buy(self,price,ACTIVES,ACTION):
       # ACTION:"put"/"call"
        while True:
            #print("try buy")
            while True:
                try:
                    self.api.buy(price, OP_code.ACTIVES[ACTIVES], "turbo", ACTION)
                    break
                except:
                    logging.error('buy error')
                    pass
            while self.api.buy_successful==None:
                pass
            if self.api.buy_successful:
                break
            else:
                #print("reconnect")#if fail to buy we need to reconnect
                #print("buy return fail")
                logging.error('fail buy need reconnect')
                self.connect()
        #print("buy ok")
    def call(self,price,ACTIVES):
        while True:
            try:
                self.api.buy(price,OP_code.ACTIVES[ACTIVES], "turbo", "call")
            except:
                pass
    def put(self,price,ACTIVES):
        while True:
            try:
                self.api.buy(price,OP_code.ACTIVES[ACTIVES], "turbo", "put")
            except:
                pass


