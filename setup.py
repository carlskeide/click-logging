from setuptools import setup

__version__ = "0.7.4"

setup(name="click_logging",
      version=__version__,
      description='Stylish logger for click-based applications',
      author='Carl Skeide',
      py_modules=["click_logging"],
      install_requires=["click"])
