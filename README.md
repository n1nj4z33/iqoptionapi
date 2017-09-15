# IQ Option API
[![Build Status](https://travis-ci.org/n1nj4z33/iqoptionapi.svg?branch=master)](https://travis-ci.org/n1nj4z33/iqoptionapi)
[![Documentation Status](https://readthedocs.org/projects/iqoptionapi/badge/?version=latest)](http://iqoptionapi.readthedocs.io/?badge=latest)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/b46b3e988c76418ab1e724f36c7b7e05/badge.svg)](https://www.quantifiedcode.com/app/project/b46b3e988c76418ab1e724f36c7b7e05)
[![PyPI version](https://badge.fury.io/py/iqoptionapi.svg)](https://badge.fury.io/py/iqoptionapi)

A friendly python wrapper around the [IQ Option API](https://iqoption.com).

Information about basic usage you can find on [Wiki](https://github.com/n1nj4z33/iqoptionapi/wiki)

Auto generated Sphinx documentation you can  find [here](http://iqoptionapi.readthedocs.io/).

### Installation
```
pip install iqoptionapi
```

### A small example

    from iqoptionapi.api import IQOptionAPI
    import datetime
    import time
    import logging
    logging.basicConfig(format='%(asctime)s %(message)s')

    api = IQOptionAPI("iqoption.com", "email", "Password")

    api.connect()
    time.sleep(0.5)
    print 'Your current blance is: {:.2f}'.format(api.profile.balance)

    #How to get candles data: 1st param is the asset or so
    #second is the interval size of the candles (currently 60 secs)
    #and the third one is the amount of candles we would like to have
    api.getcandles(1, 60, 25)
    #somehow we need that wait. Don't ask me why. Otherwise we have no data
    time.sleep(0.25)
    data = api.candles.candles_data
    for candles in data:
        st = datetime.datetime.fromtimestamp(candles[0]+60).strftime('%Y-$
       '''
        candles data
        0th entry: timestamp of candle
        1st entry: where candles starts in the interval
        2nd entry: where candles finishes in the interval
        3rd entry: upper wick
        4th entry: lower wick
        '''
        print st, candles

    #let's do some buys :D
    while api.timesync.server_datetime.second != 48:
        print api.timesync.server_datetime.second
    #The first one is the money you want to set
    #2nd is the asset. Check constants.ASSETS for the values
    #3rd is the which mode. Turbo is for binary. Don't ask me why
    #4th is either call or put
    api.buy(1, 1, "turbo", "call")
    time.sleep(0.5)


