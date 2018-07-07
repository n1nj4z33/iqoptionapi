import datetime
import time
from iqoptionapi.ws.chanels.base import Base


class Get_positions(Base):
    name = "sendMessage"
    def __call__(self,instrument_type):
        data = {
            "name":"get-positions",
            "body":{
                "instrument_type":instrument_type,
                "user_balance_id":int(self.api.profile.balance_id)
                }
        }
        self.send_websocket_request(self.name, data)

class Get_position_history(Base):
    name = "sendMessage"
    def __call__(self,instrument_type):
        data = {
            "name":"get-position-history",
            "body":{
                "instrument_type":instrument_type,
                "user_balance_id":int(self.api.profile.balance_id)
                }
        }
        self.send_websocket_request(self.name, data)
 
 