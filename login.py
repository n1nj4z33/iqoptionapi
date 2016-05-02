# -*- coding: utf-8 -*-
"""Module for IQ option login resource."""

from iqoption_api.resource import Resource


class Login(Resource):
    # pylint: disable=too-few-public-methods
    """Class for IQ option login resource."""

    url = "login"

    def _post(self, data=None, headers=None):
        """
        Send post request

        :returns: :class:`requests.Response`.
        """
        return self.send_http_request("POST", data=data)

    def __call__(self, username, password):
        """
        Method to api login.

        :returns: :class:`requests.Response`.
        """
        data = dict(email=username,
                    password=password)
        return self._post(data=data)    
