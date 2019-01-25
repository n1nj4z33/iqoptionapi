from iqoptionapi.ws.chanels.base import Base
import time

class GetDeferredOrders(Base):
    
    name = "sendMessage"

    def __call__(self,instrument_type):
     
        data = {"name":"get-deferred-orders",
                "version":"1.0",
                "body":{
                        "user_balance_id":int(self.api.profile.balance_id),
                        "instrument_type":instrument_type                 
                     
                        }
                }

        self.send_websocket_request(self.name, data)
