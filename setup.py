from setuptools import setup, find_packages

setup(name="click_logging",
      version='0.7.0',
      options={},
      description='Stylish logger for click-based applications',
      author='Carl Skeide',
      packages=find_packages(),
      install_requires=["logging",
                        "click"])
