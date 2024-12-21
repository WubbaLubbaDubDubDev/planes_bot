import json
import random
import os

from TGDeviceGen.models.android import Android
from TGDeviceGen.models.chrome import Chrome
from TGDeviceGen.models.manufacturer import Manufacturer
from TGDeviceGen.models.device import Device
from TGDeviceGen.models.telegram import Telegram
from TGDeviceGen.models.unique_device import UniqueDevice


class Generator:
    def __init__(self):
        self.__android_versions = self.__load_android_versions()
        self.__manufacturers = self.__load_manufacturers()
        self.__telegram_versions = self.__load_telegram_versions()
        self.__chrome_versions = self.__load_chrome_versions()

    def __load_manufacturers(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "source", "manufacturers", "manufacturers.json")
        with open(path, encoding='utf-8') as file:
            manufacturers_dict = json.load(file)
        manufacturers = []
        for manufacturer_name in list(manufacturers_dict.keys()):
            manufacturer = Manufacturer(name=manufacturer_name)
            for device_data in manufacturers_dict[manufacturer_name]:
                model = device_data["Name"]
                android_versions = device_data["AndroidVersions"]
                android_versions = [android for android in self.__android_versions if android.version
                                    in android_versions]
                performance_class = device_data["PerformanceClass"]
                device = Device(model=model, android_versions=android_versions,
                                performance_class=performance_class)
                manufacturer.add_device(device)
            manufacturers.append(manufacturer)
        return manufacturers

    @staticmethod
    def __load_android_versions():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "source", "android", "versions.json")
        with open(path, encoding='utf-8') as file:
            android_versions_dict = json.load(file)
        android_versions = []
        for version in list(android_versions_dict.keys()):
            sdk = android_versions_dict[version]["SDK"]
            android = Android(version=version, sdk=sdk)
            android_versions.append(android)
        return android_versions

    @staticmethod
    def __load_telegram_versions():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "source", "telegram", "versions.json")
        with open(path, encoding='utf-8') as file:
            telegram_versions_list = json.load(file)
        telegram_versions = []
        for version in telegram_versions_list:
            telegram_version = Telegram(version=version)
            telegram_versions.append(telegram_version)
        return telegram_versions

    @staticmethod
    def __load_chrome_versions():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "source", "browsers", "chrome", "android_stable.json")
        with open(path, encoding='utf-8') as file:
            chrome_versions_list = json.load(file)
        chrome_versions = []
        for version in list(chrome_versions_list.keys()):
            builds = chrome_versions_list[version]["Builds"]
            for build in builds:
                chrome_version = Chrome(version=version, build=build)
                chrome_versions.append(chrome_version)
        return chrome_versions

    @staticmethod
    def generate_app_version():
        major = random.randint(1, 10)
        minor = random.randint(0, 99)
        patch = random.randint(0, 999)
        return f"{major}.{minor}.{patch}"

    def generate_unique_device(self):
        manufacturer = random.choice(self.__manufacturers)
        device = random.choice(manufacturer.devices)
        manufacturer_name = manufacturer.name
        android = random.choice(device.android_versions)
        model = device.model
        performance_class = device.performance_class
        telegram = random.choice(self.__telegram_versions)
        chrome_version = random.choice(self.__chrome_versions)
        app_version = self.generate_app_version()
        unique_device = UniqueDevice(manufacturer=manufacturer_name, android=android, model=model,
                                     performance_class=performance_class, telegram=telegram,
                                     chrome=chrome_version, app_version=app_version)
        return unique_device

    @staticmethod
    def save_device(file_path: str, unique_device: UniqueDevice):
        android_version = unique_device.android.version
        android_sdk = unique_device.android.sdk
        telegram_version = unique_device.telegram.version
        chrome_version = unique_device.chrome.version
        chrome_build = unique_device.chrome.build

        device = {"android": {"version": android_version,
                              "sdk": android_sdk},
                  "manufacturer": unique_device.manufacturer,
                  "model": unique_device.model,
                  "performance_class": unique_device.performance_class,
                  "telegram": {"version": telegram_version},
                  "chrome": {"version": chrome_version,
                             "build": chrome_build},
                  "app_version": unique_device.app_version}

        with open(file_path, "w") as file:
            json.dump(device, file, indent=4)

    @staticmethod
    def load(file_path: str):
        with open(file_path, "r") as file:
            data = json.load(file)

        android_version = data["android"]["version"]
        android_sdk = data["android"]["sdk"]
        android = Android(version=android_version,
                          sdk=android_sdk)

        telegram_version = data["telegram"]["version"]
        telegram = Telegram(version=telegram_version)

        chrome_version = data["chrome"]["version"]
        chrome_build = data["chrome"]["build"]
        chrome = Chrome(version=chrome_version,
                        build=chrome_build)

        unique_device = UniqueDevice(android=android,
                                     manufacturer=data["manufacturer"],
                                     model=data["model"],
                                     performance_class=data["performance_class"],
                                     telegram=telegram,
                                     chrome=chrome,
                                     app_version=data["app_version"])

        return unique_device
