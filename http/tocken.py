# -*- coding: utf-8 -*-
"""Module for IQ Option http tocken resource."""

from iqapi.http.resource import Resource
from iqapi.http.auth import Auth


class Tocken(Resource):
    """Class for IQ Option http tocken resource."""
    # pylint: disable=too-few-public-methods

    url = "/".join((Auth.url, "tocken"))

    def __init__(self, api):
        super(Tocken, self).__init__(api)

    def _get(self):
        """Send get request for IQ Option API tocken http resource.

        :returns: The instace of :class:`requests.Response`.
        """
        return self.send_http_request("GET")

    def __call__(self):
        """Method to get IQ Option API tocken http request.

        :returns: The instance of :class:`requests.Response`.
        """
        return self._get()
