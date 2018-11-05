#python

import datetime
import time
from iqoptionapi.ws.chanels.base import Base
class Change_Tpsl(Base):
    name = "sendMessage"
    def __call__(self,position_id,stop_lose,take_profit,use_trail_stop):
        data = {
            "name":"change-tpsl",
            "version":"1.0",
            "body":{
                "extra":{
                    "stop_lose_type": "price",
                    "take_profit_type": "price"
                    }, 
                "position_id": position_id,
                "stop_lose": stop_lose,
                "take_profit": take_profit,
                "use_trail_stop": use_trail_stop
            }
        }
        self.send_websocket_request(self.name, data)
 
 