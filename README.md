# IQ Option API

(Frok from [n1nj4z33/iqoptionapi](https://github.com/n1nj4z33/iqoptionapi))

!Rolling release!

This API is Diligent development!! 

Please Read Document

update:2018/6/19
news: 
* fix reconnect problem

sucess on python3.6.4

---

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
I_want_money=IQ_Option("email","password",reconnect_limit=11)
goal="EURUSD"
print("get candles")
print(I_want_money.get_candles(goal,60,111,time.time()))
```
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
### View all ACTIVES Name
you will get right all ACTIVES and code

[ACTIVE_CODE.txt](ACTIVE_CODE.txt)

```python
print(I_want_money.get_all_ACTIVES_OPCODE())
```

---
 

### For Options
Sample call or put
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
### Candle

#### get candles
!!!pay attention!!! get_candles can not get "real time data" ,it will late about 30sec

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

#### get  realtime candles
you will get ""latest"" DATA
```python
I_want_money.start_candles_stream("EURUSD")
print(I_want_money.get_realtime_candles("EURUSD"))
I_want_money.stop_candles_stream("EURUSD")
```
#### get all realtime candles
```python
I_want_money.start_all_candles_stream()
print(I_want_money.get_all_realtime_candles())
I_want_money.stop_all_candles_stream()
```

#### collect realtime candles
i will do for loop untill collect time out
```python
I_want_money.start_candles_stream("EURUSD")
print(I_want_money.collect_realtime_candles("EURUSD",10.5))
#I_want_money.collect_realtime_candles("EURUSD",time)
#time:collect time(sec) can use float :11.2       
I_want_money.stop_candles_stream("EURUSD")

```

#### collect realtime candles on thread

##### Sample 
```
from iqoptionapi.stable_api import IQ_Option
import logging
import time
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
I_want_money=IQ_Option("email","password")

I_want_money.start_candles_stream("EURUSD")
thread=I_want_money.collect_realtime_candles_thread_start("EURUSD",100)


I_want_money.start_candles_stream("USDTRY")
thread2=I_want_money.collect_realtime_candles_thread_start("USDTRY",100)



time.sleep(3)
#Do some thing
ans=I_want_money.thread_collect_realtime.items()

for k, v in ans:
    print (k, v)




I_want_money.collect_realtime_candles_thread_stop(thread)
I_want_money.stop_candles_stream("EURUSD")


I_want_money.collect_realtime_candles_thread_stop(thread2)
I_want_money.stop_candles_stream("USDTRY")
```
collect data in thread with out wait
```python
I_want_money.start_candles_stream("EURUSD")
thread=I_want_money.collect_realtime_candles_thread_start("EURUSD",100)
#I_want_money.collect_realtime_candles_thread_start("EURUSD",maxdict)
#maxdict:Set the maximum candles you want collect to prevent memory overflow
#maxdict :because dict doing del and add len(maxdict) will change
#sample maxdict set 100 maxdict will get 100~101 for Guarantee max at less have 100
######do some thing#######
time.sleep(3)
######do some thing#######
print(I_want_money.thread_collect_realtime)
I_want_money.collect_realtime_candles_thread_stop(thread) 
I_want_money.stop_candles_stream("EURUSD")

```
---
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

### check win
```python
I_want_money.check_win(23243221)
#""you need to get id_number from buy function""
#I_want_money.check_win(id_number)
#this function will do loop check your bet until if win/equal/loose
```
 



 
 
    
