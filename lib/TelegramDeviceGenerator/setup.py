from setuptools import setup, find_packages

setup(
    name='TGDeviceGen',
    version='0.4',
    packages=find_packages(),
    package_data={
        'TGDeviceGen': ['source/android/**/*.json', "source/browsers/**/*.json", "source/telegram/**/*.json",
                        "source/manufacturers/**/*.json"],
    },
)