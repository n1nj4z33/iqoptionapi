# IQ Option API

(Frok from [n1nj4z33/iqoptionapi](https://github.com/n1nj4z33/iqoptionapi))

!Rolling release!

This API is Diligent development!! 

Please Read Document

update:2018/5/4

sucess on python3.6.4

---

## Installation & GET new version
```
sudo pip3 install -U git+git://github.com/Lu-Yi-Hsun/iqoptionapi.git
```

---
## Littile sample
```
from iqoptionapi.stable_api import IQ_Option
I_want_money=IQ_Option("email","password")
goal="EURUSD"
print("get candles")
print(I_want_money.get_candles(goal,60,111,time.time()))
```
---
## Document

### Import 
```
from iqoptionapi.stable_api import IQ_Option
```
---
### Debug mode on

```
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
```
---
### Login
!!!

Login NOT support SMS Authorization yet

I suggest close it because your robot will stop to wait you to check sms code (on phone)....

!!!

```
I_want_money=IQ_Option("email","password")
```
---
### View all ACTIVES Name
```
will add..
```
---
### Buy 

#### For Options

```
I_want_money.buy(Money,ACTIVES,ACTION,expirations_mode,force_buy)
                #Money:How many you want to buy type(number)
                #ACTIVES:sample input "EURUSD" OR "EURGBP"....
                #ACTION:"call"/"put" type(str)
                #expirations_mode:1~9
                #force_buy= True: if fail try buy untill sucess 
                            False:if fail break
                #return:True/False if sucess or not
```
___

#### For Forex&CFD&Crypto&Digital
```
will add ......

```

---

### get candles
!!!pay attention!!! get_candles can not get "real time data" ,it will late about 30sec

if you very care about real time you need use 

"get realtime candles" OR "collect realtime candles"

sample 

""now"" time 1:30:45sec

1.  you want to get  candles 1:30:45sec now
    
    you may get 1:30:15sec data have been late approximately 30sec

2.  you want to get  candles 1:00:33sec 

    you will get the right data

```
I_want_money.get_candles(ACTIVES,interval,count,endtime)
            #ACTIVES:sample input "EURUSD" OR "EURGBP".... you need to look constants.py file type(str)
            #interval:duration of candles
            #count:how many candles you want to get from now to past
            #endtime:get candles from past to "endtime"
```

### get  realtime candles
you will get ""latest"" DATA
```
I_want_money.start_candles_stream("EURUSD")
print(I_want_money.get_realtime_candles("EURUSD"))
I_want_money.stop_candles_stream("EURUSD")
```
### get all realtime candles
```
I_want_money.start_all_candles_stream()
print(I_want_money.get_all_realtime_candles())
I_want_money.stop_all_candles_stream()
```

### collect realtime candles
i will do for loop untill collect time out
```
I_want_money.start_candles_stream("EURUSD")
print(I_want_money.collect_realtime_candles("EURUSD",10.5))

#I_want_money.collect_realtime_candles("EURUSD",time)
#time:collect time(sec) can use float :11.2              

I_want_money.stop_candles_stream("EURUSD")

```

### collect realtime candles on thread
collect data in thread with out wait
```
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

```
---

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
 

### Change real/practice Account
```
I_want_money.change_balance(MODE)
                        #MODE: "PRACTICE"/"REAL"
```

# Will Add new option........

### sell
```
```

### for CRYPTO


### for CFD

### for FOREX

### for Digital
