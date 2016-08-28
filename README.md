# IQ Option API
[![Build Status](https://travis-ci.org/n1nj4z33/iqapi.png)](https://travis-ci.org/n1nj4z33/iqapi)
[![Documentation Status](https://readthedocs.org/projects/iqapi/badge/?version=latest)](http://iqapi.readthedocs.io/en/latest/?badge=latest)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/b46b3e988c76418ab1e724f36c7b7e05/badge.svg)](https://www.quantifiedcode.com/app/project/b46b3e988c76418ab1e724f36c7b7e05)

A friendly python wrapper around the [IQ Option API](https://iqoption.com).

Auto generated Sphinx documentation you can  find here [Documentation](http://http://iqapi.readthedocs.io/).

###Basic usage:
```
from iqapi.api import IQOptionAPI

api = IQOptionAPI("iqoption.com", "username", "password")
api.connect()
```
