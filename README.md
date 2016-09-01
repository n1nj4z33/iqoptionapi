# IQ Option API
[![Build Status](https://travis-ci.org/n1nj4z33/iqoptionapi.svg?branch=master)](https://travis-ci.org/n1nj4z33/iqoptionapi)
[![Documentation Status](https://readthedocs.org/projects/iqoptionapi/badge/?version=latest)](http://iqoptionapi.readthedocs.io/en/latest/?badge=latest)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/b46b3e988c76418ab1e724f36c7b7e05/badge.svg)](https://www.quantifiedcode.com/app/project/b46b3e988c76418ab1e724f36c7b7e05)

A friendly python wrapper around the [IQ Option API](https://iqoption.com).

Auto generated Sphinx documentation you can  find [here](http://iqoptionapi.readthedocs.io/en/latest/).

###Basic usage:
```
from iqoptionapi.api import IQOptionAPI

api = IQOptionAPI("iqoption.com", "username", "password")
api.connect()
```
