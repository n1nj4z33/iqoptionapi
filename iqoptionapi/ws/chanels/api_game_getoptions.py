#python
"""Module for IQ option candles websocket chanel."""

from iqoptionapi.ws.chanels.base import Base
import time

class Getoptions(Base):

    name = "api_game_getoptions"

    def __call__(self,limit):
    
        data = {"limit":int(limit),
               "user_balance_id":int(self.api.profile.balance_id)
                }

        self.send_websocket_request(self.name, data)
