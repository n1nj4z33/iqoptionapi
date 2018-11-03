# IQ Option API

last Version:2.1.4

This API is Diligent development!!

Please Read Document

last update:2018/11/2

Version 2.1.4

[* add get_optioninfo(only for binary option)](#optioninfo)

[* add PURCHASE TIME sample](#purchase)

[* add get_server_timestamp](#timestamp)


sucess on python3.6.5

---
## About API
```python
#hight level api ,This api is write base on ""iqoptionapi.api" for more easy
from iqoptionapi.stable_api import IQ_Option
#low level api
from iqoptionapi.api import IQOptionAPI
```
```bash
.
├── docs
├── iqoptionapi(API code)
    ├── http(doing http get/post)
    └── ws
        ├── chanels(Doing websocket action)
        └── objects(Get back data from websocket action)
```

## Installation & GET new version
For Python3
```bash
sudo pip3 install -U git+git://github.com/Lu-Yi-Hsun/iqoptionapi.git
```
For Python2
```bash
sudo pip2 install -U git+git://github.com/Lu-Yi-Hsun/iqoptionapi.git
```
---
## Littile sample
```python
import time
from iqoptionapi.stable_api import IQ_Option
I_want_money=IQ_Option("email","password")
goal="EURUSD"
print("get candles")
print(I_want_money.get_candles(goal,60,111,time.time()))
```
---
## Find ticker symbol
when you buy some thing you need to know ""ticker"" symbol

if you want to buy 
""Alphabet Inc.""
ticker symbol:""GOOGL""
buysomeapi("GOOGL")

you can find ticker symbol here 

[https://iqoption.com/en/assets](https://iqoption.com/en/assets)


---

## Document

### Import 
```python
from iqoptionapi.stable_api import IQ_Option
```
---
### Debug mode on

```python
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
```
---
### Login
!!!

Login NOT support SMS Authorization yet

I suggest close it because your robot will stop to wait you to check sms code (on phone)....

!!!

```python
I_want_money=IQ_Option("email","password")
```
---
### Reconnect&check connect

some time connect will close so this way can check connect and reconnect

sample

```python
I_want_money=IQ_Option("email","password")
#check if connect
if I_want_money.check_connect()==False:
    I_want_money.connect()#if not connect it will reconnect
```

 
 
---
### Check version

```python
I_want_money=IQ_Option("email","password")
print(I_want_money.__version__)
```

---
### View all ACTIVES Name
you will get right all ACTIVES and code

[ACTIVE_CODE.txt](ACTIVE_CODE.txt)

```python
print(I_want_money.get_all_ACTIVES_OPCODE())
```

---
 

### For Options

#### BUY

Sample
```python
from iqoptionapi.stable_api import IQ_Option
import logging
import time
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
I_want_money=IQ_Option("email","pass")
goal="EURUSD"
print("get candles")
print(I_want_money.get_candles(goal,60,111,time.time()))
Money=1
ACTIVES="EURUSD"
ACTION="call"#or "put"
expirations_mode=1
force_buy= "True"
I_want_money.buy(Money,ACTIVES,ACTION,expirations_mode,force_buy)
```

```python
I_want_money.buy(Money,ACTIVES,ACTION,expirations,force_buy)
                #Money:How many you want to buy type(int)
                #ACTIVES:sample input "EURUSD" OR "EURGBP".... you can view by get_all_ACTIVES_OPCODE
                #ACTION:"call"/"put" type(str)
                #expirations:input minute,careful too large will false to buy(Closed market time)thank Darth-Carrotpie's code (int)https://github.com/Lu-Yi-Hsun/iqoptionapi/issues/6
                #force_buy= True: if fail try buy untill sucess 
                            #False:if fail break
                #return:(True/False,id):if sucess return (True,id_number) esle return(False,None)
```

#### check win

(only for option)

It will do loop until get win or loose

:exclamation:

it have a little problem when network close and reconnect miss get "listInfoData"

this function will doing Infinity loop

```python
I_want_money.check_win(23243221)
#""you need to get id_number from buy function""
#I_want_money.check_win(id_number)
#this function will do loop check your bet until if win/equal/loose
```
##### check_win_v2

(only for option)

more better way

an other way to fix that(implement by get_betinfo)

input by int

```python
I_want_money.check_win_v2(23243221)
#""you need to get id_number from buy function""
#I_want_money.check_win_v2(id_number)
#this function will do loop check your bet until if win/equal/loose
```
#### get_betinfo

(only for option)

it will get infomation about Bet by "id"

:exclamation:

if your bet(id) not have answer yet(game_state) or wrong id it will return False
input by int

```python
 
isSuccessful,dict=I_want_money.get_betinfo(4452272449)
#I_want_money.get_betinfo 
#INPUT: int
#OUTPUT:isSuccessful,dict

```
#### <a id=optioninfo>get_optioninfo</a>

input how many data you want to get from Trading History(only for binary option)

```
print(I_want_money.get_optioninfo(10))
```
___

### For Digital
#### Sample

```python
from iqoptionapi.stable_api import IQ_Option
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
I_want_money=IQ_Option("email","password")
strike_list=I_want_money.get_strike_list_data("EURUSD",1)
print("Strike List")
for i in strike_list:
    print("key",i,"value",strike_list[i])
#Choose first Strike List
instrument_id=strike_list[list(strike_list)[0]]
I_want_money.buy_digit(3,"put",instrument_id)
```
#### Get strike list 
```python
strike_list=I_want_money.get_strike_list_data("EURUSD",1)
#strike_list=I_want_money.get_strike_list_data(ACTIVE,expirations)
#ACTIVE:"EURUSD"....
#expirations: it seem only 1 and 5 for choose
#return:dict{strike data,instrument_id}
```
#### Buy digit
```python
I_want_money.buy_digit(3,"put",instrument_id)
#I_want_money.buy_digit(price,direction,instrument_id)
#price:how many you want to buy
#direction:"call"/"put"
#instrument_id:you need get from strike list
```

---
### For Forex&Stock&Commodities&Crypto&ETFs

#### you need to check Asset is open or close!
![](image/asset_close.png)


#### About instrument_type
||Forex|Stock|Commodities|Crypto|ETFs
--|--|--|--|--|--|
instrument_type|"forex"|"cfd"|"cfd"|"crypto"|"cfd"

#### About active
if you want to buy ""Alphabet Inc.""

find ticker symbol

[https://iqoption.com/en/assets](https://iqoption.com/en/assets)

you can find "Alphabet Inc."'s ticker symbol is "GOOGLE"

instrument_id="GOOGL"

#### Sample
```python
from iqoptionapi.stable_api import IQ_Option
import logging
import time
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
I_want_money=IQ_Option("email","password")

instrument_type="crypto"
instrument_id="BTCUSD"
side="buy"#sell
type="market"#limit
amount=11
limit_price=2#for limit ,if you choose market this not work,
leverage=3#you can get more information in get_available_leverages()
stop_lose_price=1#
take_profit_price=20000#

check,order_id=I_want_money.buy_order(instrument_type,instrument_id,side,type,amount,limit_price,leverage,stop_lose_price,take_profit_price)
print(I_want_money.get_order(order_id))
print(I_want_money.get_positions("crypto"))
print(I_want_money.get_position_history("crypto"))
print(I_want_money.get_available_leverages("crypto","BTCUSD"))
print(I_want_money.close_position(order_id))
print(I_want_money.get_overnight_fee("crypto","BTCUSD"))
```
 



#### Buy

return (True/False,buy_order_id/False)

if Buy sucess return (True,buy_order_id)

```python
instrument_type="crypto"
instrument_id="BTCUSD"
side="buy"#sell
type="market"#limit
amount=11#How many money you want investment
limit_price=2#for limit ,if you choose market this not work,
leverage=3#you can get more information in get_available_leverages()
stop_lose_price=1#stop lose price
take_profit_price=20000#take profit price

I_want_money.buy_order(instrument_type,instrument_id,side,type,amount,limit_price,leverage,stop_lose_price,take_profit_price)
```
#### get_order
get infomation about buy_order_id

return (True/False,get_order,None)

```python
I_want_money.get_order(buy_order_id)
```
#### get_positions

you will get there data

![](image/get_positions.png)

return (True/False,get_positions,None)

```python
I_want_money.get_positions(instrument_type)
```

#### get_position_history

you will get there data

![](image/get_position_history.png)

return (True/False,position_history,None)

```python
I_want_money.get_position_history(instrument_type)
```


#### get_available_leverages

get available leverages

return (True/False,available_leverages,None)

```python
I_want_money.get_available_leverages(instrument_type,actives)
```
#### cancel_order

you will do this

![](image/cancel_order.png)

return (True/False)

```python
I_want_money.cancel_order(buy_order_id)
```

#### close_position

you will do this

![](image/close_position.png)

return (True/False)

```python
I_want_money.close_position(buy_order_id)
```

#### get_overnight_fee

return (True/False,overnight_fee,None)

```python
I_want_money.get_overnight_fee(instrument_type,active)
```
---
---

### Candle

#### get candles
:exclamation:

 get_candles can not get "real time data" ,it will late about 30sec

if you very care about real time you need use 

"get realtime candles" OR "collect realtime candles"

sample 

""now"" time 1:30:45sec

1.  you want to get  candles 1:30:45sec now
    
    you may get 1:30:15sec data have been late approximately 30sec

2.  you want to get  candles 1:00:33sec 

    you will get the right data

```python
I_want_money.get_candles(ACTIVES,interval,count,endtime)
            #ACTIVES:sample input "EURUSD" OR "EURGBP".... youcan
            #interval:duration of candles
            #count:how many candles you want to get from now to past
            #endtime:get candles from past to "endtime"
```
:exclamation:
try this code to get more than 1000 candle
```python
from iqoptionapi.stable_api import IQ_Option
import time
I_want_money=IQ_Option("email","password")
end_from_time=time.time()
ANS=[]
for i in range(70):
    data=I_want_money.get_candles("EURUSD", 60, 1000, end_from_time)
    ANS =data+ANS
    end_from_time=int(data[0]["from"])-1
print(ANS)
```

#### get realtime candles

##### Sample 
```python
from iqoptionapi.stable_api import IQ_Option
import logging
import time
#logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
print("login...")
I_want_money=IQ_Option("email","password")
goal="EURUSD"
size="all"#size=[1,5,10,15,30,60,120,300,600,900,1800,3600,7200,14400,28800,43200,86400,604800,2592000,"all"]
maxdict=10
print("start stream...")
I_want_money.start_candles_stream(goal,size,maxdict)
#DO something
print("Do something...")
time.sleep(10)

print("print candles")
cc=I_want_money.get_realtime_candles(goal,size)
for k in cc:
    print(goal,"size",k,cc[k])
print("stop candle")
I_want_money.stop_candles_stream(goal,size)
```
 
##### start_candles_stream
 
* input:
    * goal:"EURUSD"...
    * size:[1,5,10,15,30,60,120,300,600,900,1800,3600,7200,14400,28800,43200,86400,604800,2592000,"all"]
    * maxdict:set max buffer you want to save

size

![](image/time_interval.png)

##### get_realtime_candles
* input:
    * goal:"EURUSD"...
    * size:[1,5,10,15,30,60,120,300,600,900,1800,3600,7200,14400,28800,43200,86400,604800,2592000,"all"]
* output:
    * dict
##### stop_candles_stream
* input:
    * goal:"EURUSD"...
    * size:[1,5,10,15,30,60,120,300,600,900,1800,3600,7200,14400,28800,43200,86400,604800,2592000,"all"]

---
### time

#### <a id=timestamp> get_server_timestamp</a>
the get_server_timestamp time is sync with iqoption
```python
I_want_money.get_server_timestamp()
```

#### <a id=purchase>Purchase Time</a>
this sample get the Purchase time clock
```python
import time

#get the end of the timestamp by expiration time
def get_expiration_time(t):
    exp=time.time()#or I_want_money.get_server_timestamp() to get more Precision
    if (exp % 60) > 30:
        end = exp - (exp % 60) + 60*(t+1)
    else:
        end = exp - (exp % 60)+60*(t)
    return end
    
expiration_time=2

end_time=0
while True:
    if end_time-time.time()-30<=0:
        end_time = get_expiration_time(expiration_time)
    print(end_time-time.time()-30)
    time.sleep(1)
```

---
### Get mood

Sample

```python
from iqoptionapi.stable_api import IQ_Option
I_want_money=IQ_Option("email","password")
goal="EURUSD"
I_want_money.start_mood_stream(goal)
print(I_want_money.get_traders_mood(goal))
I_want_money.stop_mood_stream(goal)
```

#### get_traders_mood


get  percent of higher(call)

if you want to know percent of lower(put) just 1-higher
```python
I_want_money.get_traders_mood(goal)
#input:input "EURUSD" OR "EURGBP".... you can view by get_all_ACTIVES_OPCODE
#output:(float) the higher(call)%
#if you want to know lower(put)% try 1-I_want_money.get_traders_mood(goal)
```
#### get_all_traders_mood
get all you start mood
```python
I_want_money.get_all_traders_mood(goal)
#output:(dict) all mood you start
```

### Account
#### get all profit
```python
I_want_money.get_all_profit()
#return type(dict) sample:dict["EURUSD"]=0.85 
```
#### get balance
```python
I_want_money.get_balance()
```
#### Change real/practice Account
```python
I_want_money.change_balance(MODE)
                        #MODE: "PRACTICE"/"REAL"
```

---


 
 
    
