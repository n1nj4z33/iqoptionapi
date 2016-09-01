# -*- coding: utf-8 -*-
"""The IQ Option API package setup."""
from setuptools import (setup, find_packages)

setup(
    name="iqoptionapi",
    version="0.1",
    description="The IQ Option API.",
    url="https://github.com/n1nj4z33/iqoptionapi",
    author="n1nj4z33",
    author_email="n1nj4z33@gmail.com",
    packages=find_packages() + ["."],
    package_dir={"": "."},
    install_requires=["setuptools"],
    zip_safe=False
)
