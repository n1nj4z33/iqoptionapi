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


Check if a trade has been won or lost:
ou can give the result by using the 'win' variable which returns either 'equal' (if the trade is ongoing or a draw), 'win' (if the trade was a win), or 'loose' (if the trade was a loss)

    self.api.listinfodata.current_listinfodata.win

or

    self.api.listinfodata.get_listinfodata(foo)

For more information on what you can actually get, you can use this JSON data which got extracted by frxncisjoseph while testing.

    "name":"listInfoData","msg":[{"amount":1000000,"id":2095724656,"refund":0,"currency":"USD","currency_char":"$","active_id":1,"active":"EURUSD","value":1.07736,"exp_value":1077360,"dir":"call","created":1489706346,"expired":1489706400,"type_name":"turbo","type":"front.TU","profit":100,"profit_amount":1,"win_amount":1.74,"loose_amount":0,"sum":1,"win":"equal","now":1489706346,"user_id":0,"game_state":0,"profit_income":174,"profit_return":0,"option_type_id":3,"site_id":1,"is_demo":false,"user_balance_id":0,"client_platform_id":9,"re_track":"null","params":null}]}

Here is a piece of code in order to check if the buy order went through and to check how the order is doing:
    
    api.buy(1, 816, "turbo", "call")    
    time.sleep(0.5)

    while api.buySuccessful in [None, False]:
    ....#Could do another buy order, or something else!

    print api.listinfodata.current_listinfodata.win
