# -*- coding: utf-8 -*-
"""Module for base IQ option resource."""


class Resource(object):
    """Class for base IQ option resource."""

    def __init__(self, api):
        """
        :param api: :class:`IQOptionAPI <iqoption_api.api.IQOptionAPI>`.
        """
        self.api = api

    @property
    def session(self):
        """Property to get session.

        :returns: The session object.
        """
        return self.api.get_session()

    def send_http_request(self, method, data=None, params=None, headers=None):
        """
        Send request to IQ option server.

        :param str method: The HTTP request method.
        :param dict data: (optional) The HTTP request data.
        :param dict params: (optional) The HTTP request params.
        :param dict headers: (optional) The HTTP request headers.

        :returns: :class:`requests.Response`.
        """
        return self.api.send_http_request(self, method, data=data, params=params, headers=headers)
