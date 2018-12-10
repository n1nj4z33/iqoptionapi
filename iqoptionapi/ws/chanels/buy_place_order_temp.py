import datetime
import time
from iqoptionapi.ws.chanels.base import Base

#work for forex digit cfd(stock)

class Buy_place_order_temp(Base):
    name = "sendMessage"
    def __call__(self,instrument_type,instrument_id,side,type,amount,leverage,limit_price,stop_price,stop_lose_price,take_profit_price):
        data = {
        "name": "place-order-temp",
        "version":"3.0",
        "body":{
            "instrument_type":str(instrument_type),
            "instrument_id":str(instrument_id),
            "side":str(side),
            "type":type,
            "amount":int(amount),
            "user_balance_id":int(self.api.profile.balance_id),
            "client_platform_id":"9",
            "leverage":int(leverage),
            "limit_price":int(limit_price),
            "stop_price":int(stop_price),
            "stop_lose_price":float(stop_lose_price),
            "take_profit_price":float(take_profit_price),
            "use_token_for_commission":"false",
            "auto_margin_call":"false"    
            }
        }
        self.send_websocket_request(self.name, data)
 
