# Get start

## document version

last update:2020/3/13

Version:6.8.9

fix some ssl problem

Version:6.8.8

more stable 

fix login and auto logout

fix check_connect

Version:6.8.7

add get_leader_board
 

## install iqoptionapi

download the source code and run this

```
python setup.py install
```
## little sample

```python
import time
from iqoptionapi.stable_api import IQ_Option
I_want_money=IQ_Option("email","password")
I_want_money.connect()#connect to iqoption
goal="EURUSD"
print("get candles")
print(I_want_money.get_candles(goal,60,111,time.time()))
```

## Import

```python
from iqoptionapi.stable_api import IQ_Option
```
## Login

I_want_money.connect() will return (check,reason)

if connect sucess return True,None

if connect fail return False,reason

```python
from iqoptionapi.stable_api import IQ_Option
import logging

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
I_want_money=IQ_Option("email","password")
check, reason=I_want_money.connect()#connect to iqoption
print(check, reason)
```
## Debug mode on

```python
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
```
 
## Connect&Check connect

some time connect will close so this way can check connect and reconnect

try close your network and restart network in this sample

```python
from iqoptionapi.stable_api import IQ_Option
error_password="""{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
iqoption = IQ_Option("email", "password")
check,reason=iqoption.connect()
if check:
    print("Start your robot")
    #if see this you can close network for test
    while True: 
        if iqoption.check_connect()==False:#detect the websocket is close
            print("try reconnect")
            check,reason=iqoption.connect()         
            if check:
                print("Reconnect successfully")
            else:
                if reason==error_password:
                    print("Error Password")
                else:
                    print("No Network")
        
else:
    
    if reason=="[Errno -2] Name or service not known":
        print("No Network")
    elif reason==error_password:
        print("Error Password")
```
## set_session

Default User-Agent is "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"

```python
from iqoptionapi.stable_api import IQ_Option
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
 
I_want_money=IQ_Option("email","password")

#Default is "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"

header={"User-Agent":r"Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"}
cookie={"I_want_money":"GOOD"}

I_want_money.set_session(header,cookie)

I_want_money.connect()#connect to iqoption
```

## Check version

```python
from iqoptionapi.stable_api import IQ_Option
print(IQ_Option.__version__)
```

## Check connect

return True/False
```
print(I_want_money.check_connect())
```

## Reconnect

```python
I_want_money.connect()
```

## time

get_server_timestamp
the get_server_timestamp time is sync with iqoption

```python
I_want_money.get_server_timestamp()
```
 