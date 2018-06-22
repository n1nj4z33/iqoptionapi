#python
import datetime
from iqoptionapi.ws.chanels.base import Base
class Strike_list(Base):
    name = "sendMessage"
    
    def __call__(self,name,expiration):  
        exp=self.get_expiration_time(expiration)
        data = {
            "name": "get-strike-list",
            "body":{"type":"digital-option",
                    "underlying":name,
                    "expiration":int(exp)*1000,
                    "expiration_type":"PT"+str(expiration)+"M"}
        }
        self.send_websocket_request(self.name, data)

    def get_expiration_time(self, duration):
        exp=int(self.api.timesync.server_timestamp)
        if duration>=1 and duration<=5:
            #Round to next full minute
            if (exp % 60) > 50:
                exp = exp - (exp % 60) + 60*(duration+1)
            else:
                exp = exp - (exp % 60)+60*(duration)
        return exp
'''
{"name":"sendMessage",
"request_id":"523",
"msg":{
        "name":"get-strike-list",
        "version":"3.0",
        "body":{
            "type":"digital-option"
            ,"underlying":"AUDCAD",
            "expiration":1527141960000,
            "expiration_type":"PT1M"}}}
'''