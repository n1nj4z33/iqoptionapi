#python

import time
import datetime

from iqoptionapi.ws.objects.base import Base
class Strike_list_data(Base):
    """Class for IQ Option TimeSync websocket object."""

    def __init__(self):
        super(Strike_list_data, self).__init__()
        self.__All_data = {}
     
 
    def get_All_data(self):
        """Property to get server timestamp.

        :returns: The server timestamp.
        """
        return self.__All_data

    
    def put_All_data(self,ACTIVE, expiration,data):
        """Method to set server timestamp."""
        self.__All_data[ACTIVE,expiration]=data

    def del_data(self,ACTIVE, expiration):
        del self.__All_data[ACTIVE,expiration]