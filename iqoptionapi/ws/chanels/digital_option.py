#python

import datetime
import time
from iqoptionapi.ws.chanels.base import Base
import iqoptionapi.global_value as global_value
#work for forex digit cfd(stock)

class Digital_options_place_digital_option(Base):
    name = "sendMessage"
    def __call__(self,instrument_id,amount):
        data = {
        "name": "digital-options.place-digital-option",
        "version":"1.0",
        "body":{
            "user_balance_id":int(global_value.balance_id),
            "instrument_id":str(instrument_id),
            "amount":str(amount)
            
            }
        }
        self.send_websocket_request(self.name, data)
 
class Digital_options_close_position(Base):
    name = "sendMessage"
    def __call__(self,position_id):
        data = {
        "name": "digital-options.close-position",
        "version":"1.0",
        "body":{
            "position_id":int(position_id)
            }
        }
        self.send_websocket_request(self.name, data)
 
