#python
from iqoptionapi.api import IQOptionAPI
import iqoptionapi.constants as OP_code
import threading
import time
import logging
import operator
class IQ_Option:
    __version__="2.1.3"
    def __init__(self,email,password):
        self.size=[1,5,10,15,30,60,120,300,600,900,1800,3600,7200,14400,28800,43200,86400,604800,2592000]
        self.email=email
        self.password=password
        self.suspend = 0.5
        self.thread=None
        self.subscribe_candle=[]
        self.subscribe_candle_all_size=[]
        self.subscribe_mood=[]
    
        #--start
        self.connect()
        self.update_ACTIVES_OPCODE()
        self.get_balance_id()

    def get_server_time(self):
        return self.api.timesync.server_timestamp
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
                
            except:
                logging.error('**error** connect() fail')
            if check==True:
                #-------------reconnect subscribe_candle
                try:
                    for ac in self.subscribe_candle:
                        sp=ac.split(",")    
                        self.start_candles_one_stream(sp[0],sp[1])
                except:
                    pass
                #-----------------
                try:
                    for ac in self.subscribe_candle_all_size:
                        self.start_candles_all_size_stream(ac)
                except:
                    pass
                #-------------reconnect subscribe_mood
                try:
                    for ac in self.subscribe_mood:
                        self.start_mood_stream(ac)
                except:
                    pass
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
            try:
                self.api.get_instruments(types)
                start=time.time()
                while self.api.instruments==None and time.time()-start<10:
                    pass
            except:
                logging.error('**error** api.get_instruments need reconnect')
                self.connect()
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
        
        while True :
            self.api.api_option_init_all_result = None
            while True:
                try:
                    self.api.get_api_option_init_all()      
                    break
                except:
                    logging.error('**error** get_all_init need reconnect')
                    self.connect()
                    time.sleep(5)
            start=time.time()
            while True:
                if time.time()-start>30:
                    logging.error('**warning** get_all_init late 30 sec')
                    break
                try:
                    if self.api.api_option_init_all_result != None:
                        break
                except:
                    pass  
            try:           
                if self.api.api_option_init_all_result["isSuccessful"]==True:
                    return self.api.api_option_init_all_result
            except:
                pass
   
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
    def get_balance_id(self):
        self.api.profile.balance_id=None
        while True:
            try:
                respon=self.get_profile()
                self.api.profile.balance_id=respon["result"]["balance_id"]
                break
            except:
                logging.error('**error** get_balance()')
      
            time.sleep(self.suspend)
        return self.api.profile.balance

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
                while self.check_connect and self.api.candles.candles_data==None:
                    pass
                if self.api.candles.candles_data!=None:
                    break          
            except:
                logging.error('**error** get_candles need reconnect')
                self.connect()
         
        return self.api.candles.candles_data
#######################################################
#______________________________________________________
#_____________________REAL TIME CANDLE_________________   
#______________________________________________________
#######################################################
    def start_candles_stream(self,ACTIVE,size,maxdict):
        
        if size=="all":
            for s in self.size:
                self.full_realtime_get_candle(ACTIVE,s,maxdict)
                self.api.real_time_candles_maxdict_table[ACTIVE][s]=maxdict
            self.start_candles_all_size_stream(ACTIVE)
        elif size in self.size:
            self.api.real_time_candles_maxdict_table[ACTIVE][size]=maxdict
            self.full_realtime_get_candle(ACTIVE,size,maxdict)
            self.start_candles_one_stream(ACTIVE,size)
            
        else:
            logging.error('**error** start_candles_stream please input right size')

    def stop_candles_stream(self,ACTIVE,size):
        if size=="all":
            self.stop_candles_all_size_stream(ACTIVE)
        elif size in self.size:
            self.stop_candles_one_stream(ACTIVE,size)
        else:
            logging.error('**error** start_candles_stream please input right size')

    def get_realtime_candles(self,ACTIVE,size):
        if size=="all":
            try:
                return self.api.real_time_candles[ACTIVE]
            except:
                logging.error('**error** get_realtime_candles() size="all" can not get candle')
                return False    
        elif  size in self.size:
            try:
                return self.api.real_time_candles[ACTIVE][size]
            except:
                logging.error('**error** get_realtime_candles() size='+str(size)+' can not get candle')
                return False     
        else:
            logging.error('**error** get_realtime_candles() please input right "size"')
    def get_all_realtime_candles(self):
        return self.api.real_time_candles
################################################
#---------REAL TIME CANDLE Subset Function---------
################################################
#---------------------full dict get_candle-----------------------
    def full_realtime_get_candle(self,ACTIVE,size,maxdict):
        candles=self.get_candles(ACTIVE,size,maxdict,self.api.timesync.server_timestamp)
        for can in candles:
            self.api.real_time_candles[str(ACTIVE)][int(size)][can["from"]]=can

#------------------------Subscribe ONE SIZE-----------------------
    def start_candles_one_stream(self,ACTIVE,size):
        if (str(ACTIVE+","+str(size)) in self.subscribe_candle)==False:
            self.subscribe_candle.append((ACTIVE+","+str(size)))
        start=time.time()
        self.api.candle_generated_check[str(ACTIVE)][int(size)]= {}
        while True:
            if time.time()-start>20:
                logging.error('**error** start_candles_one_stream late for 20 sec')
                return False
            try:
                if self.api.candle_generated_check[str(ACTIVE)][int(size)] == True:
                    return True
            except:
                pass
            try:
            
                self.api.subscribe(OP_code.ACTIVES[ACTIVE],size)
            except:
                logging.error('**error** start_candles_stream reconnect')
                self.connect()
            time.sleep(1)

    def stop_candles_one_stream(self,ACTIVE,size):
        if ((ACTIVE+","+str(size)) in self.subscribe_candle)==True:
             self.subscribe_candle.remove(ACTIVE+","+str(size))
        while True:
            try:
                if self.api.candle_generated_check[str(ACTIVE)][int(size)] == {}:
                    return True
            except:
                pass
            self.api.candle_generated_check[str(ACTIVE)][int(size)]= {}
            self.api.unsubscribe(OP_code.ACTIVES[ACTIVE],size)
            time.sleep(self.suspend*10)
#------------------------Subscribe ALL SIZE-----------------------
    def start_candles_all_size_stream(self,ACTIVE):
        self.api.candle_generated_all_size_check[str(ACTIVE)]={}
        if (str(ACTIVE) in self.subscribe_candle_all_size)==False:
            self.subscribe_candle_all_size.append(str(ACTIVE))
        start=time.time()
        while True:
            if time.time()-start>20:
                logging.error('**error** fail '+ACTIVE+' start_candles_all_size_stream late for 10 sec')
                return False
            try:
                if self.api.candle_generated_all_size_check[str(ACTIVE)] == True:
                    return True       
            except:
                pass
            try:
                self.api.subscribe_all_size(OP_code.ACTIVES[ACTIVE])
            except:
                logging.error('**error** start_candles_all_size_stream reconnect')
                self.connect()
            time.sleep(1)
    def stop_candles_all_size_stream(self,ACTIVE):
        if (str(ACTIVE) in self.subscribe_candle_all_size)==True:
            self.subscribe_candle_all_size.remove(str(ACTIVE))
        while True:
            try:
                if self.api.candle_generated_all_size_check[str(ACTIVE)] == {}:
                    break
            except:
                pass
            self.api.candle_generated_all_size_check[str(ACTIVE)] = {}
            self.api.unsubscribe_all_size(OP_code.ACTIVES[ACTIVE])
            time.sleep(self.suspend*10)
#---------------------------------------------------------------------
 

          
         
        

################################################
################################################            
#-----------------------------------------------

#-----------------traders_mood----------------------
    def start_mood_stream(self,ACTIVES):
        if ACTIVES in self.subscribe_mood==False:
            self.subscribe_mood.append(ACTIVES)
        
        while True:
            self.api.subscribe_Traders_mood(OP_code.ACTIVES[ACTIVES])
            try:
                self.api.traders_mood[OP_code.ACTIVES[ACTIVES]]
                break
            except:
                time.sleep(1) 

    def stop_mood_stream(self,ACTIVES):
        if ACTIVES in self.subscribe_mood==True:
            del self.subscribe_mood[ACTIVES]     
        self.api.unsubscribe_Traders_mood(OP_code.ACTIVES[ACTIVES])
    def get_traders_mood(self,ACTIVES):
        #return highter %
        return self.api.traders_mood[OP_code.ACTIVES[ACTIVES]]
    def get_all_traders_mood(self):
        #return highter %
        return self.api.traders_mood
##############################################################################################
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
            time.sleep(self.suspend)

    def get_betinfo(self,id_number):
        #INPUT:int
        while True:
            self.api.game_betinfo.isSuccessful=None
            start=time.time()
            try:
                self.api.get_betinfo(id_number)
            except:
                logging.error('**error** def get_betinfo  self.api.get_betinfo reconnect')
                self.connect()
            while self.api.game_betinfo.isSuccessful==None:
                if time.time()-start>10:
                    logging.error('**error** get_betinfo time out need reconnect')
                    self.connect()
                    self.api.get_betinfo(id_number)
                    time.sleep(self.suspend*10)                       
            if self.api.game_betinfo.isSuccessful==True:
                return self.api.game_betinfo.isSuccessful,self.api.game_betinfo.dict
            else:
                return self.api.game_betinfo.isSuccessful,None
            time.sleep(self.suspend*10)
        

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

#----------------------------------------------------------       
#-----------------BUY_for__Forex__&&__stock(cfd)__&&__ctrpto
    def buy_order(self,instrument_type,instrument_id,side,type,amount,limit_price,leverage,stop_lose_price,take_profit_price):        
        self.api.buy_order_id=None
        self.api.buy_order(instrument_type=instrument_type,instrument_id=instrument_id,side=side,type=type,amount=amount,limit_price=limit_price,stop_price=0,leverage=leverage,stop_lose_price=stop_lose_price,take_profit_price=take_profit_price)
        while self.api.buy_order_id==None:
            pass
        check,data=self.get_order(self.api.buy_order_id)
        while data["status"]=="pending_new":
            check,data=self.get_order(self.api.buy_order_id)
            time.sleep(1)
 
        if check:
            if data["status"]!="rejected":
                return True,self.api.buy_order_id
            else:
                return False,None
        else:
            
            return False,None
        

    def get_order(self,buy_order_id):
        #self.api.order_data["status"] 
        #reject:you can not get this order
        #pending_new:this order is working now
        #filled:this order is ok now
        #new
        self.api.order_data=None
        self.api.get_order(buy_order_id)
        while self.api.order_data==None:
            pass
        if self.api.order_data["status"]==2000:
            return True,self.api.order_data["msg"]
        else:
            return False,None
    #this function is heavy
    
    def get_positions(self,instrument_type):
        self.api.positions=None
        self.api.get_positions(instrument_type)
        while self.api.positions==None:
            pass
        if self.api.positions["status"]==2000:
            return True,self.api.positions["msg"]
        else:
            return False,None
    #this function is heavy 
    def get_position_history(self,instrument_type):
        self.api.position_history=None
        self.api.get_position_history(instrument_type)
        while self.api.position_history==None:
            pass
        
        if self.api.position_history["status"]==2000:
            return True,self.api.position_history["msg"]
        else:
            return False,None
    
    def get_available_leverages(self,instrument_type,actives):
        self.api.available_leverages=None
        self.api.get_available_leverages(instrument_type,OP_code.ACTIVES[actives])
        while self.api.available_leverages==None:
            pass
        if self.api.available_leverages["status"]==2000:
            return True,self.api.available_leverages["msg"]
        else:
            return False,None

    def cancel_order(self,buy_order_id):
        self.api.order_canceled=None
        self.api.cancel_order(buy_order_id)
        while self.api.order_canceled==None:
            pass
        if self.api.order_canceled["status"]==2000:
            return True
        else:
            return False
    def close_position(self,buy_order_id):
        check,data=self.get_order(buy_order_id)
        if data["position_id"]!=None:
            self.api.close_position_data=None
            self.api.close_position(data["position_id"])
            while self.api.close_position_data==None:
                pass
            if self.api.close_position_data["status"]==2000:
                return True
            else:
                return False
        else:
            return False
    def get_overnight_fee(self,instrument_type,active):
        self.api.overnight_fee=None
        self.api.get_overnight_fee(instrument_type,OP_code.ACTIVES[active])
        while self.api.overnight_fee==None:
            pass
        if self.api.overnight_fee["status"]==2000:
            return True,self.api.overnight_fee["msg"]
        else:
            return False,None
        

