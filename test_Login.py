import unittest
 
import os
 
import logging
import os, sys
sys.path.insert(0, os.path.abspath(".."))
from iqoptionapi.stable_api import IQ_Option
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')
 
email=os.getenv("email")
password=os.getenv("password")


I_want_money=IQ_Option(email,password)

