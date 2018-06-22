import datetime
import time
from iqoptionapi.ws.chanels.base import Base

class Game_betinfo(Base):
    name = "api_game_betinfo"
    def __call__(self, id_number_list):
        data = {"currency": "USD"}
        for idx, val in enumerate(id_number_list):
            data["id["+str(idx)+"]"]=int(val)
        self.send_websocket_request(self.name, data)