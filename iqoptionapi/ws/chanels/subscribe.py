"""Module for IQ option subscribe websocket chanel."""

from iqoptionapi.ws.chanels.base import Base


class Subscribe(Base):
    """Class for IQ option candles websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "subscribeMessage"

    def __call__(self, active_id,size=1):
       #{"name":"subscribeMessage","msg":{"name":"candle-generated","params":{"routingFilters":{"active_id":1,"size":1}}}}
 
        data = {"name":"candle-generated",
                "params":{
                       "routingFilters":{
                                        "active_id":active_id,
                                        "size":size
                                        }
                        }
                }

        self.send_websocket_request(self.name, data)

