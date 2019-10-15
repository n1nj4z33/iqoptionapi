import unittest
 
import os
from iqoptionapi.stable_api import IQ_Option

 
class TestLogin(unittest.TestCase):
  
    def test_login(self):
        email=os.getenv("email")
        password=os.getenv("password")
        I_want_money=IQ_Option(email,password)
        self.assertEqual(I_want_money.check_connect(), True)
         
 
if __name__ == '__main__':
    unittest.main()