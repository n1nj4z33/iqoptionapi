# Digital


## Nearest strike mode
![](image/near.png)
### sample

```python
from iqoptionapi.stable_api import IQ_Option
import time
import random
I_want_money=IQ_Option("email","password")
I_want_money.connect()#connect to iqoption
ACTIVES="EURUSD"
duration=1#minute 1 or 5
amount=1
I_want_money.subscribe_strike_list(ACTIVES,duration)
#get strike_list
data=I_want_money.get_realtime_strike_list(ACTIVES, duration)
print("get strike data")
print(data)
"""data
{'1.127100': 
    {  'call': 
            {   'profit': None, 
                'id': 'doEURUSD201811120649PT1MC11271'
            },   
        'put': 
            {   'profit': 566.6666666666666, 
                'id': 'doEURUSD201811120649PT1MP11271'
            }	
    }............
} 
"""
#get price list
price_list=list(data.keys())
#random choose Strategy
choose_price=price_list[random.randint(0,len(price_list)-1)]
#get instrument_id
instrument_id=data[choose_price]["call"]["id"]
#get profit
profit=data[choose_price]["call"]["profit"]
print("choose you want to buy")
print("price:",choose_price,"side:call","instrument_id:",instrument_id,"profit:",profit)
#put instrument_id to buy
buy_check,id=I_want_money.buy_digital(amount,instrument_id)
polling_time=5
if buy_check:
    print("wait for check win")
    #check win
    while True:
        check_close,win_money=I_want_money.check_win_digital_v2(id,polling_time)
        if check_close:
            if float(win_money)>0:
                win_money=("%.2f" % (win_money))
                print("you win",win_money,"money")
            else:
                print("you loose")
            break
    I_want_money.unsubscribe_strike_list(ACTIVES,duration)
else:
    print("fail to buy,please run again")
```

### Get all strike list data

smaple 
```python
from iqoptionapi.stable_api import IQ_Option
import time
I_want_money=IQ_Option("email","password")
I_want_money.connect()#connect to iqoption
ACTIVES="EURUSD"
duration=1#minute 1 or 5
I_want_money.subscribe_strike_list(ACTIVES,duration)
while True:
    data=I_want_money.get_realtime_strike_list(ACTIVES, duration)
    for price in data:
        print("price",price,data[price])
    time.sleep(5)
I_want_money.unsubscribe_strike_list(ACTIVES,duration)
```
#### subscribe_strike_list()

```python
I_want_money.subscribe_strike_list(ACTIVES,duration)
```

#### get_realtime_strike_list

you need call subscribe_strike_list() before get_realtime_strike_list()
```python
I_want_money.get_realtime_strike_list(ACTIVES,duration)
```

#### unsubscribe_strike_list()
```python
I_want_money.unsubscribe_strike_list(ACTIVES,duration)
```
### buy_digital()

```python
buy_check,id=I_want_money.buy_digital(amount,instrument_id)
#get instrument_id from I_want_money.get_realtime_strike_list
```

## Current price mode

![](image/spot.png)



### buy_digital_spot
buy the digit in current price

return check and id

```python
from iqoptionapi.stable_api import IQ_Option
 
I_want_money=IQ_Option("email","password")
I_want_money.connect()#connect to iqoption
ACTIVES="EURUSD"
duration=1#minute 1 or 5
amount=1
action="call"#put
print(I_want_money.buy_digital_spot(ACTIVES,amount,action,duration))
```

### get_digital_spot_profit_after_sale()

get Profit After Sale(P/L)

![](image/profit_after_sale.png)

sample 

```python
from iqoptionapi.stable_api import IQ_Option 
I_want_money=IQ_Option("email","passord")
ACTIVES="EURUSD"
duration=1#minute 1 or 5
amount=100
action="put"#put
 
I_want_money.subscribe_strike_list(ACTIVES,duration)
_,id=I_want_money.buy_digital_spot(ACTIVES,amount,action,duration) 
 
while True:
    PL=I_want_money.get_digital_spot_profit_after_sale(id)
    if PL!=None:
        print(PL)
```

### get_digital_current_profit()

```python
from iqoptionapi.stable_api import IQ_Option
import time
import logging
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
I_want_money=IQ_Option("email","password")
I_want_money.connect()#connect to iqoption
ACTIVES="EURUSD"
duration=1#minute 1 or 5
I_want_money.subscribe_strike_list(ACTIVES,duration)
while True:
    data=I_want_money.get_digital_current_profit(ACTIVES, duration)
    print(data)#from first print it may be get false,just wait a second you can get the profit
    time.sleep(1)
I_want_money.unsubscribe_strike_list(ACTIVES,duration)
```

## check win for digital

### check_win_digital()

this api is implement by get_digital_position()

this function is polling , so need to set polling time
```python
I_want_money.check_win_digital(id,polling_time)#get the id from I_want_money.buy_digital
```
### check_win_digital_v2()

this api is asynchronous get id data,it only can get id data before you call the buy action. if you restart the program,the asynchronous id data can not get again,so check_win_digital_v2 may not working,so you need to use "check_win_digital"!

```python
 I_want_money.check_win_digital_v2(id)#get the id from I_want_money.buy_digital
#return:check_close,win_money
#return sample
#if you loose:Ture,o
#if you win:True,1232.3
#if trade not clode yet:False,None
```

sample code

```python
from iqoptionapi.stable_api import IQ_Option
import logging
import random
import time
import datetime
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
I_want_money=IQ_Option("email","password")
I_want_money.connect()#connect to iqoption
ACTIVES="EURUSD"
duration=1#minute 1 or 5
amount=1
action="call"#put
_,id=(I_want_money.buy_digital_spot(ACTIVES,amount,action,duration))
print(id)
if id !="error":
    while True:
        check,win=I_want_money.check_win_digital_v2(id)
        if check==True:
            break
    if win<0:
        print("you loss "+str(win)+"$")
    else:
        print("you win "+str(win)+"$")
else:
    print("please try again")
```

## close_digital_option()

```python
I_want_money.close_digital_option(id)
```

## get digital data

smaple1
```python
from iqoptionapi.stable_api import IQ_Option
import logging
import time
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
I_want_money=IQ_Option("email","password")
I_want_money.connect()#connect to iqoption
ACTIVES="EURUSD-OTC"
duration=1#minute 1 or 5
amount=1
action="call"#put
from datetime import datetime
 
_,id=I_want_money.buy_digital_spot(ACTIVES,amount,action,duration) 

while True:
    check,_=I_want_money.check_win_digital(id)
    if check:
        break
print(I_want_money.get_digital_position(id))
print(I_want_money.check_win_digital(id))
```

sample2

```python
print(I_want_money.get_positions("digital-option"))
print(I_want_money.get_digital_position(2323433))#in put the id
print(I_want_money.get_position_history("digital-option"))
```