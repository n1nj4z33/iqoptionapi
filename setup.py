# -*- coding: utf-8 -*-
"""The IQ Option API package setup."""
from setuptools import (setup, find_packages)

setup(
    name="iqoption_api",
    version="0.1",
    description="The IQ Option API.",
    url="https://github.com/n1nj4z33/iqoption_api",
    author="n1nj4z33",
    author_email="n1nj4z33@gmail.com",
    packages=find_packages() + ["."],
    # package_data = find_package_data(),
    # include_package_data = True,
    package_dir={"": "."},
    install_requires=["setuptools"],
    zip_safe=False
)
