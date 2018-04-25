"""Module for IQ option subscribe websocket chanel."""

from iqoptionapi.ws.chanels.base import Base


class Subscribe(Base):
    """Class for IQ option subscribe websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "subscribe"

    def __call__(self, chanel_name):
        """Method to send message to subscribe websocket chanel.

        :param chanel_name: The websocket chanel name to subsribe.
        """
        self.send_websocket_request(self.name, chanel_name)
class subscribeMessage_candle_generated(Base):
    """Class for IQ option candles websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "subscribeMessage"

    def __call__(self, active_id):
       #{"name":"subscribeMessage","msg":{"name":"candle-generated","params":{"routingFilters":{"active_id":1,"size":1}}}}
 
        data = {"name":"candle-generated",
                "params":{
                       "routingFilters":{
                                        "active_id":active_id,
                                        "size":1
                                        }
                        }
                }

        self.send_websocket_request(self.name, data)
