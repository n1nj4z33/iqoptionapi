"""The python wrapper for IQ Option API package setup."""
from setuptools import (setup, find_packages)

setup(
    name="iqoptionapi",
    version="2.1.2",
    packages=find_packages(),
    install_requires=["pylint","requests","websocket-client==0.47"],
    include_package_data = True,
    description="The python wrapper for IQ Option API.more stable",
    long_description="The python wrapper IQ Option API.more stable",
    url="https://github.com/Lu-Yi-Hsun/iqoptionapi",
    author="Lu-Yi-Hsun",
    author_email="yihsun1992@gmail.com",
    zip_safe=False
)
