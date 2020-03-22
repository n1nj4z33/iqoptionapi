"""Module for IQ Option buyV2 websocket chanel."""
import datetime
import time
from iqoptionapi.ws.chanels.base import Base
import logging
from iqoptionapi.expiration import get_expiration_time
from datetime import datetime,timedelta
import iqoptionapi.global_value  as global_value

class Buyv2(Base):
    """Class for IQ option buy websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "buyV2"

    def __call__(self, price, active, direction,duration):
        """Method to send message to buyv2 websocket chanel.

        :param price: The buying price.
        :param active: The buying active.
        :param direction: The buying direction.
        """
        # thank Darth-Carrotpie's code 
        #https://github.com/Lu-Yi-Hsun/iqoptionapi/issues/6
      
        exp,idx=get_expiration_time(int(self.api.timesync.server_timestamp),duration)  
        
        if idx<5:
            option="turbo"
        else:
            option="binary"



        data = {
            "price": price,
            "act": active,
            "exp":int(exp),
            "type": option,
            "direction": direction.lower(),
            "user_balance_id":int(global_value.balance_id),
            "time": self.api.timesync.server_timestamp
        }

        self.send_websocket_request(self.name, data)

    # thank Darth-Carrotpie's code 
    #https://github.com/Lu-Yi-Hsun/iqoptionapi/issues/6
"""    def get_expiration_time(self, duration):
        exp=int(self.api.timesync.server_timestamp)
        if duration>=1 and duration<=5:
            option="turbo"
            #Round to next full minute
            #datetime.datetime.now().second>30
            if (exp % 60) > 30:
                exp = exp - (exp % 60) + 60*(duration+1)
            else:
                exp = exp - (exp % 60)+60*(duration)
        elif duration > 5:
            option = "binary"
            period = int(round(duration / 15))
            tmp_exp = exp - (exp % 60)#nuima sekundes
            tmp_exp = tmp_exp - (tmp_exp%3600)#nuimam minutes
            j=0
            while exp > tmp_exp + (j)*15*60:#find quarter
                j = j+1
            if exp - tmp_exp > 5 * 60:
                quarter = tmp_exp + (j)*15*60
                exp = quarter + period*15*60
            else:
                quarter = tmp_exp + (j+1)*15*60
                exp = quarter + period*15*60
        else:
            logging.error("ERROR get_expiration_time DO NOT LESS 1")
            exit(1)
        return exp, option"""