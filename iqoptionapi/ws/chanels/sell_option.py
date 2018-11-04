 
from iqoptionapi.ws.chanels.base import Base
import time

class Sell_Option(Base):
    name = "sendMessage"
    def __call__(self, options_ids):
        """ 
        :param options_ids: list of id
        """
        data = {"name":"sell-options",
                "version":"2.0",
                "body":{
                        "options_ids":options_ids
                        }
                }

        self.send_websocket_request(self.name, data)
