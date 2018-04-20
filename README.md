# IQ Option API(Frok from [n1nj4z33/iqoptionapi]
### Installation
```
git clone https://github.com/Lu-Yi-Hsun/iqoptionapi.git
cd iqoptionapi
sudo python3 setup.py install
```

### A small example
    from iqoptionapi.api import IQOptionAPI
    import datetime
    import time
    import logging
    logging.basicConfig(format='%(asctime)s %(message)s')
    api = IQOptionAPI("iqoption.com", "email","password")
    api.connect()
    time.sleep(1.5)
    print ('Your current blance is: {:.2f}'.format(api.profile.balance))
    api.buy(1, 1, "turbo", "call")
    api.getcandles(1, 1, 3)
                #getcandles(ACTIVES,interval,count)
                #ACTIVES:look constants.py file
                #interval: time interval
                #count:how many candles you want to get from now to past
    time.sleep(2)
    data = api.candles.candles_data
    print(data)
