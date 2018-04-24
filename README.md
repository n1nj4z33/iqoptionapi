# IQ Option API(Frok from [n1nj4z33/iqoptionapi](https://github.com/n1nj4z33/iqoptionapi))
fix some thing...

sucess on python3.6.4

---

### Installation
```
git clone https://github.com/Lu-Yi-Hsun/iqoptionapi.git
cd iqoptionapi
sudo python3 setup.py install
```
---


### More stable Libary base on iqoptionapi for Robot
```
from iqoptionapi.api import IQOptionAPI
import iqoptionapi.constants as OP_code
import time
import numpy as np
import logging

class Binary_Option:
    def __init__(self,email,password):
        self.email=email
        self.password=password
        self.suspend = 0.6
        self.connect()
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
    def get_candles(self,ACTIVES,interval,count):
        while True:
            try:
                self.api.getcandles(OP_code.ACTIVES[ACTIVES], interval, count)
                break
            except:
                logging.error('fail get_candles need reconnect')
                self.connect()
                #print("get_candles error")
                pass
        while self.api.candles.candles_data==None:
            pass
        return self.api.candles.candles_data

    def get_candles_as_array(self,ACTIVES,interval,count):
        candles=self.get_candles(count,ACTIVES,interval)
        ans = np.empty(shape=(len(candles), 4))
        for idx, candle in enumerate(candles):
            ans[idx][0] = candle["open"]
            ans[idx][1] = candle["close"]
            ans[idx][2] = candle["min"]
            ans[idx][3] = candle["max"]
        return ans
    def check_win(self):
        #'win'：win the money  'equal'：no win no loose   'loose':loose the money
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

```


### login
```
I_want_money=Binary_Option("email","password")
```
### buy
```
I_want_money.buy(Money,ACTIVES,ACTION)
                #Money:How many you want to buy type(number)
                #ACTIVES:sample input "EURUSD" OR "EURGBP".... you need to look constants.py file type(str)
                #ACTION:"call"/"put" type(str)
```

### get candles
```
I_want_money.get_candles(ACTIVES,interval,count)
            #ACTIVES:sample input "EURUSD" OR "EURGBP".... you need to look constants.py file type(str)
            #interval:duration of candles
            #count:how many candles you want to get from now to past
```
### get all profit
```
I_want_money.get_all_profit()
#return type(dict) sample:dict["EURUSD"]=0.85 
```
### get balance
```
I_want_money.get_balance()
```

### check win
```
I_want_money.check_win()
#this function will do loop check your bet until if win/equal/loose
```
## Will Add new option........

### Change real/practice Account
```
```
### sell
```
```