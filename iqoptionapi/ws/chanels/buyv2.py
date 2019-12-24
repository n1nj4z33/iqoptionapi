"""Module for IQ Option buyV2 websocket chanel."""
from iqoptionapi.ws.chanels.base import Base
from iqoptionapi.expiration import get_expiration_time


class Buyv2(Base):
    """Class for IQ option buy websocket chanel."""
    # pylint: disable=too-few-public-methods

    name = "sendMessage"

    def __call__(self, price, active, direction,duration):
        """Method to send message to buyv2 websocket chanel.

        :param price: The buying price.
        :param active: The buying active.
        :param direction: The buying direction.
        """
      
        exp, idx = get_expiration_time(int(self.api.timesync.server_timestamp),duration)
        
        if idx < 5:
            option = 3  # turbo
        else:
            option = 1  # non-turbo / binary

        data = {
            "name": "binary-options.open-option",
            "version": "1.0",
            "body": {
                "user_balance_id": int(self.api.profile.balance_id),
                "active_id": active,
                "option_type_id": option,
                "direction": direction.lower(),
                "expired": int(exp),
                "refund_value": 0,
                "price": price,
                "value": 0,  # Preset to 0, don't worry won't affect the actual buy contract
                "profit_percent": 0  # IQOption accept any value lower than the actual percent, don't worry it won't affect actual earning
            }
        }

        self.send_websocket_request(self.name, data)
