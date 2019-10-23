#python
"""Module for IQ option candles websocket chanel."""

from iqoptionapi.ws.chanels.base import Base
import time

class Get_options(Base):

    name = "api_game_getoptions"

    def __call__(self,limit):
    
        data = {"limit":int(limit),
               "user_balance_id":int(self.api.profile.balance_id)
                }

        self.send_websocket_request(self.name, data)
 
class Get_options_v2(Base):
    name = "sendMessage"
    def __call__(self,limit,instrument_type):    
        data = {
            "name":"get-options" ,
            "body":{
                "limit":limit,
                "instrument_type":instrument_type,
                "user_balance_id":int(self.api.profile.balance_id)
                }
        }
        self.send_websocket_request(self.name, data)