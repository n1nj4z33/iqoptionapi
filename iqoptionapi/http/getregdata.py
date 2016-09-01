# -*- coding: utf-8 -*-
"""Module for IQ Option http getregdata resource."""

from .resource import Resource
from .register import Register


class Getprofile(Resource):
    """Class for IQ option getregdata resource."""
    # pylint: disable=too-few-public-methods

    url = "/".join((Register.url, "getregdata"))

    def _get(self):
        """Send get request for IQ Option API getregdata http resource.

        :returns: The instace of :class:`requests.Response`.
        """
        return self.send_http_request("GET")

    def __call__(self):
        """Method to get IQ Option API getregdata http request.

        :returns: The instance of :class:`requests.Response`.
        """
        return self._get()
