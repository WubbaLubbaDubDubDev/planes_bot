from TGDeviceGen.models.android import Android
from TGDeviceGen.models.chrome import Chrome
from TGDeviceGen.models.telegram import Telegram


class UniqueDevice:
    def __init__(self, android: Android,
                 manufacturer: str,
                 model: str,
                 performance_class: str,
                 telegram: Telegram,
                 chrome: Chrome,
                 app_version: str):
        self.android = android
        self.manufacturer = manufacturer
        self.model = model
        self.performance_class = performance_class
        self.telegram = telegram
        self.chrome = chrome
        self.app_version = app_version

    def get_user_agent(self):
        user_agent = (f'Mozilla/5.0 (Linux; Android {self.android.version}; K) AppleWebKit/537.36 (KHTML, like Gecko)'
                      f' Chrome/{self.chrome.build} Mobile Safari/537.36 Telegram-Android/{self.telegram.version} '
                      f'({self.manufacturer} {self.model}; Android {self.android.version}; SDK {self.android.sdk};'
                      f' {self.performance_class})')
        return user_agent

    def get_sec_ch_ua_headers(self):
        sec_ch_ua = (f'"Chromium";v="{self.chrome.version}", "Android WebView";v="{self.chrome.version}",'
                     f' "Not?A_Brand";v="99"')
        headers = {
            'Sec-CH-UA': sec_ch_ua,
            'Sec-CH-UA-Mobile': '?1',
            'Sec-CH-UA-Platform': '"Android"'
        }
        return headers

