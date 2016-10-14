"""The python wrapper for IQ Option API package setup."""
from setuptools import (setup, find_packages)

setup(
    name="iqoptionapi",
    version="0.3",
    packages=find_packages(),
    include_package_data = True,
    license="BSD License",
    description="The python wrapper for IQ Option API.",
    long_description="The python wrapper IQ Option API.",
    url="https://github.com/n1nj4z33/iqoptionapi",
    author="n1nj4z33",
    author_email="n1nj4z33@gmail.com",
    zip_safe=False
)
