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
        self.suspend = 0.5
        self.thread=None
        self.connect()
        self.thread_collect_realtime={}
        self.get_ALL_Binary_ACTIVES_OPCODE()
 
        #time.sleep(self.suspend)
    #***  
    def connect(self):
        while True:
            try:
                try:
                    self.api.close()
                except:
                    pass
                    #logging.error('**warning** self.api.close() it can ignore')
                self.api = IQOptionAPI("iqoption.com", self.email, self.password)
                self.api.timesync.server_timestamp=None
                self.api.connect()
                time.sleep(self.suspend)
                break
            except:
                logging.error('**error** connect()')
                pass
        #wait for timestamp getting
        while True:
            try:
                if self.api.timesync.server_timestamp!=None:
                    break
            except:
                pass
        

##################################################################################

    def get_all_init(self):
        self.api.api_option_init_all_result = None
        while True :
            try:
                self.api.get_api_option_init_all()      
                start=time.time()
                while True:
                    if time.time()-start>10:
                        logging.error('**warning** get_all_init late 10 sec')
                        break
                    try:
                        if self.api.api_option_init_all_result != None:
                            break
                    except:
                        pass
                if self.api.api_option_init_all_result["isSuccessful"]==True:
                    break
                else:
                    logging.error('**error** self.api.api_option_init_all_result["isSuccessful"] ==False need reconnect')
                    self.connect() 
            except:
                logging.error('**error** get_all_init need reconnect')
                self.connect()
        return self.api.api_option_init_all_result
    def get_ALL_Binary_ACTIVES_OPCODE(self):
        init_info=self.get_all_init()
        for i in init_info["result"]["binary"]["actives"]:
            OP_code.ACTIVES[(init_info["result"]["binary"]["actives"][i]["name"]).split(".")[1]]=int(i)
            
        #return OP_code.ACTIVES
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
##################################################################################################
    def get_profile(self):
        while True:
            try :
                respon=self.api.getprofile().json()
                time.sleep(self.suspend)
                if respon["isSuccessful"]==True:
                    return respon
            except:
                logging.error('**error** get_profile')
#------------------------https profile------------------------
    def get_balance(self):
        #self.api.profile.balance=None
        while True:
            try:
                respon=self.get_profile()
                self.api.profile.balance=respon["result"]["balance"]
                break
            except:
                logging.error('**error** get_balance()')
                pass
            time.sleep(self.suspend)
        return self.api.profile.balance

    def get_balances(self):
        #self.api.profile.balance=None
        while True:
            try:
                respon=self.get_profile()
                self.api.profile.balances=respon["result"]["balances"]
                break
            except:
                logging.error('**error** get_balances()')
                pass
            time.sleep(self.suspend)
        return self.api.profile.balances

    def get_balance_mode(self):
        #self.api.profile.balance_type=None
        while True:
            try:
                respon=self.get_profile()
                self.api.profile.balance_type=respon["result"]["balance_type"]
                break
            except:
                logging.error('**error** get_balance_mode()')
                pass
            time.sleep(self.suspend)   
        if self.api.profile.balance_type==1:
            return "REAL"
        elif self.api.profile.balance_type==4:
            return "PRACTICE"
#------------------------------------------------
    def change_balance(self,Balance_MODE):
        real_id=None
        practice_id=None
        while True:
            try:
                self.get_balances()
                for accunt in self.api.profile.balances:
                    if accunt["type"]==1:
                        real_id=accunt["id"]
                    if accunt["type"]==4:
                        practice_id=accunt["id"]
                break
            except:
                logging.error('**error** change_balance()')
                pass
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
                logging.error('**error** get_candles need reconnect')
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
                self.api.subscribe(OP_code.ACTIVES[ACTIVES_name])
            time.sleep(self.suspend)
    def get_all_realtime_candles(self):
        return self.api.real_time_candles
    def stop_all_candles_stream(self):
        while self.api.real_time_candles != {}:
            self.api.real_time_candles = {}
            time.sleep(self.suspend)
            for ACTIVES_name in OP_code.ACTIVES:
                self.api.unsubscribe(OP_code.ACTIVES[ACTIVES_name])
    
                    ##one
    def start_candles_stream(self,ACTIVES):
        while self.api.real_time_candles == {}:
            time.sleep(self.suspend)
            self.api.subscribe(OP_code.ACTIVES[ACTIVES])

    def get_realtime_candles(self,ACTIVES):
        while True:
            try:
                return self.api.real_time_candles[ACTIVES]
            except:
                logging.error('**error** get_realtime_candles()')
                pass
    def stop_candles_stream(self,ACTIVES):
        while self.api.real_time_candles != {}:
            self.api.real_time_candles = {}
            time.sleep(self.suspend)
            self.api.unsubscribe(OP_code.ACTIVES[ACTIVES])
###################################collect realtime###################################
                #####dict controler####
    def dict_queue_add(self,dict,ACTIVES,maxdict,key,value):
        while True:
            if len(dict)<=maxdict:
                dict[(ACTIVES,key)]=value
                break
            else:
                #del mini key
                del dict[sorted(dict.keys(), reverse=False)[0]]



    def thread_realtime(self,ACTIVES,maxdict):
        t = threading.currentThread()
        while getattr(t,"do_run",True):
            candles=self.get_realtime_candles(ACTIVES)
            self.dict_queue_add(dict=self.thread_collect_realtime,ACTIVES=ACTIVES,maxdict=maxdict,key=candles["at"],value=candles)
        #self.thread_collect_realtime={}

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


    def check_win(self):
        #'win'：win money 'equal'：no win no loose   'loose':loose money
        self.api.listinfodata.__init__()
        start=time.time()
        while True:
            try:
                state=self.api.listinfodata.current_listinfodata.game_state
                if state==1:
                    break
            except:
                pass
        return self.api.listinfodata.current_listinfodata.win
    def buy(self,price,ACTIVES,ACTION,expirations_mode,force_buy=True):
        self.api.buy_successful==None
        while True:
            while True:
                try:
                    self.api.buy(price, OP_code.ACTIVES[ACTIVES], ACTION,expirations_mode)
                    break
                except:
                    if force_buy==False:
                        return False 
                    logging.error('self.api.buy error')
                    self.connect()
                    pass
            start=time.time()
            while self.api.buy_successful==None:
                if time.time()-start>60:
                    logging.error('check buy_successful time late 60sec')
                    break
            if self.api.buy_successful:
                return True 
            else:
                if force_buy==False:
                    return False  
                logging.error('**error** buy error...')
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


