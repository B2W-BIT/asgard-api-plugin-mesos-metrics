from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='asgard-api-plugin-metrics-mesos',
    version='0.9.0',

    description='Asgard API endpoints to get Apache Mesos metrics',
    long_description="Plugin para a Asgard API e que fornece métricas do cluster de Apache Mesos",
    url='https://github.com/B2W-BIT/asgard-api-plugin-metrics-mesos',
    # Author details
    author='Dalton Barreto',
    author_email='daltonmatos@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires = [
        "asgard-api-sdk>=0.3.0-rc1",
    ],

    entry_points={
        'asgard_api_metrics_mountpoint': [
            'init = metrics:asgard_api_plugin_init',
        ],
    },
)
