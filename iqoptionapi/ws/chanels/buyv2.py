"""Module for IQ Option buyV2 websocket chanel."""
import datetime
import time
from iqoptionapi.ws.chanels.base import Base


class Buyv2(Base):
    """Class for IQ option buy websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "buyV2"

    def __call__(self, price, active, direction,expiration_mode=1):
        """Method to send message to buyv2 websocket chanel.

        :param price: The buying price.
        :param active: The buying active.
        :param direction: The buying direction.
        """
        exp=int(self.api.timesync.server_timestamp)
     
        #exp=int(time.time())
        i=int(expiration_mode)
        if i>=1 and i<=5:
            option="turbo"
            #Round to next full minute
            if datetime.datetime.now().second > 30:
                exp = exp - (exp % 60) + 60*(i+1)
            else:
                exp = exp - (exp % 60)+60*(i)
        elif i>=6 :
            option="binary"
            tmp_exp=exp - (exp % 60)
            tmp_exp=tmp_exp-(tmp_exp%3600)#+(j)*15*60  
            j=0
            while exp>tmp_exp+(j)*15*60:#find header
                j=j+1
            header=tmp_exp+(j)*15*60
            exp=header+(i-6)*15*60
           

        
       # exp=int(self.api.timesync.expiration_timestamp)
       
        data = {
            "price": price,
            "act": active,
            "exp":exp,
            "type": option,
            "direction": direction,
            "time": self.api.timesync.server_timestamp
        }

        self.send_websocket_request(self.name, data)
