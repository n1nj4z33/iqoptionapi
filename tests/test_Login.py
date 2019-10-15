import unittest
 
import os
from iqoptionapi.stable_api import IQ_Option
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')

email=os.getenv("email")
password=os.getenv("password")
 
 
I_want_money=IQ_Option(email,password)
 
 