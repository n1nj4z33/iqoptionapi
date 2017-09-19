"""Module for IQ Option Candles websocket object."""
import json

from collections import OrderedDict

from iqoptionapi.ws.objects.base import Base


class ListInfoData(Base):
    def __init__(self):
        super(ListInfoData, self).__init__()
        self.__name = "listInfoData"
        self.__listinfodata_list = OrderedDict()

    @property
    def listinfodata_list(self):
        """Property to get listinfodata list.

        :returns: The list of listinfodata.
        """
        return self.__listinfodata_list

    @listinfodata_list.setter
    def listinfodata_list(self, listinfodata_list):
        """Method to set listinfodata list."""
        self.__listinfodata_list = listinfodata_list

    @property
    def current_listinfodata(self):
        """Method to get current iteminfodata item.

         :returns: The object of listinfodata.
         """
        return self.listinfodata_list[next(reversed(self.listinfodata_list))]

    def get_listinfodata(self, id):
        """Method to get iteminfodata item.

         :returns: The object of listinfodata.
         """
        return self.listinfodata_list[id]

    def add_listinfodata(self, new_listinfodata):
        """Method to add listinfodata."""
        #if new_listinfodata.id not in self.listinfodata_list:
        self.listinfodata_list[new_listinfodata.id] = new_listinfodata
