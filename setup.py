from setuptools import setup

import click_logging

setup(name="click_logging",
      version=click_logging.__version__,
      description='Stylish logger for click-based applications',
      author='Carl Skeide',
      py_modules=["click_logging"],
      install_requires=["logging",
                        "click"])
