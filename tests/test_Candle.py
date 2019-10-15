import unittest
import os
from iqoptionapi.stable_api import IQ_Option
import logging
import time
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
 
email=os.getenv("email")
password=os.getenv("password")
class TestCandle(unittest.TestCase):
  
    def test_Candle(self):
        #login
        I_want_money=IQ_Option(email,password)
        I_want_money.change_balance("PRACTICE")
        I_want_money.reset_practice_balance()
        self.assertEqual(I_want_money.check_connect(), True)
        #start test binary option
        opcode_dict=I_want_money.get_all_ACTIVES_OPCODE()
        for asset,value in opcode_dict.items():
            I_want_money.get_candles(asset, 60, 1000, time.time())
       
            #realtime candle
            size="all"
            I_want_money.start_candles_stream(asset,size,10)
            I_want_money.get_realtime_candles(asset,size)
            I_want_money.stop_candles_stream(asset,size)

