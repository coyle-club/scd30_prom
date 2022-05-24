#!/usr/bin/env python

from setuptools import setup

setup(
    name="scd30_prom",
    version="1.0",
    description="SCD30 measurements for prometheus",
    author="Tom Petr",
    author_email="trpetr@gmail.com",
    packages=["scd30_prom"],
    install_requires=["prometheus-client", "scd30-i2c", "click"],
    entry_points={"console_scripts": ["scd30_prom=scd30_prom:main"]},
)
