#python
import datetime
from iqoptionapi.ws.chanels.base import Base
class Digit_buy(Base):
    name = "sendMessage"
    
    def __call__(self,price,direction,instrument_id):  
        if direction=="call":
            instrument_id=instrument_id.replace("MC", "MC")
        elif direction=="put":
            instrument_id=instrument_id.replace("MC", "MP")
        else:
            print("error Digit_buy direction")
            exit(1)
        data = {
            "name": "place-order-temp",
            "body":{
                "instrument_type":"digital-option",
                "instrument_id":str(instrument_id),
                "side":"buy",
                "type":"market",
                "amount":int(price),
                "user_balance_id":int(self.api.profile.balance_id),
                "client_platform_id":"9",
                "leverage":1,
                "limit_price":0,
                "stop_price":0,
                "use_token_for_commission":"false",
                "auto_margin_call":"false" 
                   
            }
        }
        self.send_websocket_request(self.name, data)
