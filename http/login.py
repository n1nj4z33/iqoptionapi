# -*- coding: utf-8 -*-
"""Module for IQ Option http login resource."""

from iqapi.http.resource import Resource


class Login(Resource):
    """Class for IQ option login resource."""
    # pylint: disable=too-few-public-methods

    url = "login/v2"

    def _post(self, data=None, headers=None):
        """
        Send post request

        :returns: :class:`requests.Response`.
        """
        return self.send_http_request("POST", data=data, headers=headers)

    def __call__(self, username, password):
        """
        Method to api login.

        :param str username: The username of a IQ Option server.
        :param str password: The password of a IQ Option server.

        :returns: :class:`requests.Response`.
        """
        data = dict(email=username,
                    password=password)
        return self._post(data=data)
