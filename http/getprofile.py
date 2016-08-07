# -*- coding: utf-8 -*-
"""Module for IQ Option http getprofile resource."""

from iqapi.http.resource import Resource


class Getprofile(Resource):
    """Class for IQ option getprofile resource."""
    # pylint: disable=too-few-public-methods

    url = "getprofile"

    def _get(self):
        """Send get request for IQ Option API getprofile resource.

        :returns: The instace of :class:`requests.Response`.
        """
        return self.send_http_request("GET")

    def __call__(self):
        """Method to get IQ Option API getprofile http resource.

        :returns: The instance of :class:`requests.Response`.
        """
        return self._get()
