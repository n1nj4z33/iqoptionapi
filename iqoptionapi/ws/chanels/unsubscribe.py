"""Module for IQ option unsubscribe websocket chanel."""

from iqoptionapi.ws.chanels.base import Base


class Unsubscribe(Base):
    """Class for IQ option candles websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "unsubscribeMessage"

    def __call__(self, active_id,size=1):
      
        data = {"name":"candle-generated",
                "params":{
                       "routingFilters":{
                                        "active_id":active_id,
                                        "size":size
                                        }
                        }
                }

        self.send_websocket_request(self.name, data)

