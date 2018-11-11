"""Module for IQ option subscribe websocket chanel."""

from iqoptionapi.ws.chanels.base import Base
import datetime
import iqoptionapi.constants as OP_code
class Subscribe(Base):
    """Class for IQ option candles websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "subscribeMessage"

    def __call__(self, active_id,size):
       #{"name":"subscribeMessage","msg":{"name":"candle-generated","params":{"routingFilters":{"active_id":1,"size":1}}}}
 
        data = {"name":"candle-generated",
                "params":{
                       "routingFilters":{
                                        "active_id":str(active_id),
                                        "size":int(size)
                                        }
                        }
                }

        self.send_websocket_request(self.name, data)

class Subscribe_candles(Base):
    """Class for IQ option candles websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "subscribeMessage"

    def __call__(self, active_id):
       
        data = {"name":"candles-generated",
                "params":{
                       "routingFilters":{
                                        "active_id":str(active_id)
                                        }
                        }
                }

        self.send_websocket_request(self.name, data)

class Subscribe_Instrument_Quites_Generated(Base):
    name = "subscribeMessage"
    
    def __call__(self,ACTIVE):  
        data = {
            "name": "instrument-quotes-generated",
            "params":{
                "routingFilters":{
                        "active":int(OP_code.ACTIVES[ACTIVE]),
                        "kind":"digital-option",
                     
                        },
                },
            "version": "1.0"
        }
        self.send_websocket_request(self.name, data)

    def get_digital_expiration_time(self, duration):
        exp=int(self.api.timesync.server_timestamp)
        value = datetime.datetime.fromtimestamp(exp)
        minute = int(value.strftime('%M'))
        second=int(value.strftime('%S'))
        ans=exp-exp%60#delete second
        ans=ans+(duration-minute%duration)*60
        if exp>ans-10:
            ans=ans+(duration)*60
            
        return ans
