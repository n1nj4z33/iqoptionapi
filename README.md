# IQ Option API(Frok from [n1nj4z33/iqoptionapi]
### Installation
```
git clone https://github.com/Lu-Yi-Hsun/iqoptionapi.git
cd iqoptionapi
sudo python3 setup.py install
```
sucess on python3.6.4
### class
```
from iqoptionapi.api import IQOptionAPI
import iqoptionapi.constants as OP_code
import time

import logging
#logging.basicConfig(format='%(asctime)s %(message)s')
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
        return self.api.profile.balance
    def get_candles(self,count,ACTIVES):
#{'id': 10357768, 'from': 1523969349, 'to': 1523969350, 'open': 1.23524, 'close': 1.235245, 'min': 1.23524, 'max': 1.23527, 'volume': 0}
        self.api.getcandles(OP_code.ACTIVES[ACTIVES], 1, count)
        while self.api.candles.candles_data==None:
            pass
        return self.api.candles.candles_data
    def check_win(self):
        #'win'：贏  'equal'：沒輸沒贏   'loose':輸
        self.api.listinfodata.__init__()
        while True:
            try:
                state=self.api.listinfodata.current_listinfodata.game_state
                if state==1:
                    break
            except:
                pass
        return self.api.listinfodata.current_listinfodata.win
    def buy(self,price,ACTIVES,ACTION):
       # self.connect()
        old_balance=self.get_balance()
        while True:
            #print("try buy")
            while True:
                try:
                    self.api.buy(price, OP_code.ACTIVES[ACTIVES], "turbo", ACTION)
                    break
                except:
                    pass
            while self.api.buy_successful==None:
                pass
            if self.api.buy_successful:
                break
            else:
                #print("reconnect")#if fail to buy we need to reconnect
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
