#python
from iqoptionapi.api import IQOptionAPI
import iqoptionapi.constants as OP_code
import threading
import time
import logging
import operator
class IQ_Option:
    def __init__(self,email,password):
        self.email=email
        self.password=password
        self.suspend = 0.5
        self.thread=None
        self.connect()
        self.thread_collect_realtime={}
        self.update_ACTIVES_OPCODE()
        self.subscribe_table=[]
       

        #time.sleep(self.suspend)
    #***  
    def connect(self):
        while True:
            try:
                self.api.close()
            except:
                pass
                #logging.error('**warning** self.api.close() fail')
            self.api = IQOptionAPI("iqoption.com", self.email, self.password)
            check=None
            try:
                check=self.api.connect()
                for ac in self.subscribe_table:
                    self.start_candles_stream(ac)
            except:
                logging.error('**error** connect() fail')
            if check==True:
                break
            time.sleep(self.suspend*2)

    def check_connect(self):
        #True/False
        return self.api.websocket_alive()
        #wait for timestamp getting
    
#_________________________UPDATE ACTIVES OPCODE_____________________
    def get_all_ACTIVES_OPCODE(self):
        return OP_code.ACTIVES
    def update_ACTIVES_OPCODE(self):
        #update from binary option
        self.get_ALL_Binary_ACTIVES_OPCODE()
        #crypto /dorex/cfd
        self.get_all_instruments()
        dicc={}
        for lis in  sorted(OP_code.ACTIVES.items(), key=operator.itemgetter(1)):
            dicc[lis[0]]=lis[1]
        OP_code.ACTIVES=dicc
    def instruments_input(self,types):
        time.sleep(self.suspend)
        self.api.instruments=None
        while self.api.instruments==None:
            self.api.get_instruments(types)
            start=time.time()
            while self.api.instruments==None and time.time()-start<10:
                pass
        for ins in self.api.instruments["instruments"]:
            OP_code.ACTIVES[ins["id"]]=ins["active_id"]

    def get_all_instruments(self):
        self.instruments_input("crypto")
        self.instruments_input("forex")
        self.instruments_input("cfd")

    def get_ALL_Binary_ACTIVES_OPCODE(self):
        init_info=self.get_all_init()
        for i in init_info["result"]["binary"]["actives"]:
            OP_code.ACTIVES[(init_info["result"]["binary"]["actives"][i]["name"]).split(".")[1]]=int(i)
            
#_________________________self.api.get_api_option_init_all() wss______________________
    def get_all_init(self):
        self.api.api_option_init_all_result = None
        while True :
            try:
                self.api.get_api_option_init_all()      
                start=time.time()
                while True:
                    if time.time()-start>30:
                        logging.error('**warning** get_all_init late 30 sec')
                        break
                    try:
                        if self.api.api_option_init_all_result != None:
                            break
                    except:
                        self.api.get_api_option_init_all() 
                        time.sleep(self.suspend*2)
                if self.api.api_option_init_all_result["isSuccessful"]==True:
                    break
            except:
                logging.error('**error** get_all_init need reconnect')
                self.connect()
        return self.api.api_option_init_all_result
   
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
#______________________________________self.api.getprofile() https________________________________
    def get_profile(self):
        while True:
            try :
                respon=self.api.getprofile().json()
                time.sleep(self.suspend)
                if respon["isSuccessful"]==True:
                    return respon
            except:
                logging.error('**error** get_profile try reconnect')
                self.connect()
    def get_balance(self):
        self.api.profile.balance=None
        while True:
            try:
                respon=self.get_profile()
                self.api.profile.balance=respon["result"]["balance"]
                break
            except:
                logging.error('**error** get_balance()')
      
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
#________________________________________________________________________
#_______________________        CANDLE      _____________________________                
#________________________self.api.getcandles() wss________________________
    def get_candles(self,ACTIVES,interval,count,endtime):
        self.api.candles.candles_data=None
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
#______________________________________________________________
#_____________________________REAL TIME CANDLE_________________   
#______________________________________________________________
                    #all need to fixxxxxxxxxxxxxxxxxxxxxxx
                    #!!!!!!!!!!!undone!!!!!!!!!!!
    def start_all_candles_stream(self):
        while self.api.real_time_candles == {}:
            for ACTIVES_name in OP_code.ACTIVES:
                self.api.subscribe(OP_code.ACTIVES[ACTIVES_name])
                time.sleep(self.suspend)
            time.sleep(self.suspend)
    def get_all_realtime_candles(self):
        return self.api.real_time_candles
    def stop_all_candles_stream(self):
        while self.api.real_time_candles != {}:
            self.api.real_time_candles = {}
            time.sleep(self.suspend)
            for ACTIVES_name in OP_code.ACTIVES:
                self.api.unsubscribe(OP_code.ACTIVES[ACTIVES_name])
##############################################
                    ##one
    def start_candles_stream(self,ACTIVES):
        if ACTIVES in self.subscribe_table==False:
            self.subscribe_table.append(ACTIVES)
        try:
            self.api.subscribe(OP_code.ACTIVES[ACTIVES])
            start=time.time()
            while True:
                if time.time()-start>20:
                    logging.error('**error** fail '+ACTIVES+' start_candles_stream late for 10 sec')
                    return False
                try:
                    if self.api.real_time_candles[ACTIVES] != {}:
                        break
                except:
                    time.sleep(1)
                    self.api.subscribe(OP_code.ACTIVES[ACTIVES])
            if self.api.real_time_candles[ACTIVES] != {}:
                return True
        except:
            logging.error('**error** start_candles_stream reconnect')
            self.connect()
        

    def get_realtime_candles(self,ACTIVES):
        try:
            return self.api.real_time_candles[ACTIVES]
        except:
            logging.error('**error** get_realtime_candles()')
            return False

    def stop_candles_stream(self,ACTIVES):
        if ACTIVES in self.subscribe_table==True:
            del self.subscribe_table[ACTIVES]
        while True:
            try:
                if self.api.real_time_candles[ACTIVES] == {}:
                    break
            except:
                pass
            self.api.real_time_candles[ACTIVES] = {}
            time.sleep(1)
            self.api.unsubscribe(OP_code.ACTIVES[ACTIVES])
#__________________________Collect realtime_____________________________
                        
                        #______thread_____
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

#       ___None thread___
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


    def check_win(self,id_number):
        #'win'：win money 'equal'：no win no loose   'loose':loose money
        while True:
            try:
                listinfodata_dict=self.api.listinfodata.get(id_number)
                if listinfodata_dict["game_state"]==1:
                    break
            except:
                pass
        self.api.listinfodata.delete(id_number)    
        return listinfodata_dict["win"]
    def check_win_v2(self,id_number):
        while True:
            check,data=self.get_betinfo(id_number)
            if check:
                return data[str(id_number)]["win"]
            time.sleep(self.suspend*10)

    def get_betinfo(self,id_number):
        #INPUT:list/int/string
        while True:
            try:
                self.api.game_betinfo.isSuccessful=None
                start=time.time()
                self.api.get_betinfo(id_number)
                while self.api.game_betinfo.isSuccessful==None:
                    if time.time()-start>10:
                        logging.error('**error** get_betinfo time out need reconnect')
                        self.connect()
                        self.api.get_betinfo(id_number)
                        time.sleep(self.suspend*10)

                #check if id exist
                check_id_exist=False
                if type(id_number) is list:
                    for id in id_number:
                        if str(id) in self.api.game_betinfo.dict:
                            check_id_exist=True
                else:
                    if str(id_number) in self.api.game_betinfo.dict:
                        check_id_exist=True                     
                if check_id_exist:
                    if self.api.game_betinfo.isSuccessful==True:
                        return self.api.game_betinfo.isSuccessful,self.api.game_betinfo.dict
                    else:
                        return self.api.game_betinfo.isSuccessful,None
                time.sleep(self.suspend*10)
            except:
                logging.error('**error** get_betinfo reconnect')
                self.connect()

#__________________________BUY__________________________

#__________________FOR OPTION____________________________
    def buy(self,price,ACTIVES,ACTION,expirations,force_buy=True):
        self.api.buy_successful==None
        while True:
            while True:
                try:
                    self.api.buy(price, OP_code.ACTIVES[ACTIVES], ACTION,expirations)
                    break
                except:
                    if force_buy==False:
                        return (False,None) 
                    logging.error('self.api.buy error')
                    self.connect()
                    pass
            start=time.time()
            while self.api.buy_successful==None:
                if time.time()-start>60:
                    logging.error('check buy_successful time late 60sec')
                    break
            if self.api.buy_successful:
                return (True,self.api.buy_id)
            else:
                if force_buy==False:
                    return (False,None) 
                logging.error('**error** buy error...')
                self.connect()
#__________________for digit_____________
    def get_strike_list_data(self,ACTIVES,expirations):
        try:
            self.api.strike_list.del_data(ACTIVES,expirations)
        except:
            pass

        while True:
            self.api.get_strike_list(ACTIVES,expirations)
            all_strike_list_data=self.api.strike_list.get_All_data()
            try:
                return all_strike_list_data[str(ACTIVES),str(expirations)]
            except:
                pass
            time.sleep(self.suspend*3)

    def buy_digit(self,price,direction,instrument_id):
        self.api.digit_buy(price,direction,instrument_id)
    
    
 



