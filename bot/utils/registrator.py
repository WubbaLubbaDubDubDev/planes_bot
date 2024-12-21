import os.path

from better_proxy import Proxy
from telethon import TelegramClient
from TGDeviceGen.models.unique_device import UniqueDevice

from bot.config.config import settings
from bot.utils.logger import logger
from bot.utils.file_manager import save_to_json
from bot.utils.proxy_chain import ProxyChain
from bot.utils.device_manager import DeviceManager


class Registrator:
    def __init__(self, workdir: str,
                 device_manager: DeviceManager,
                 api_id: int,
                 api_hash: str,
                 skip_proxy_binding: bool = False):

        self.workdir = workdir
        self.device_manager = device_manager
        self.api_id = api_id
        self.api_hash = api_hash
        self.skip_proxy_binding = skip_proxy_binding

    async def register_session(self, proxy_chain: ProxyChain = None) -> None:
        if not self.api_id or not self.api_hash:
            raise ValueError("API_ID and API_HASH not found in the ..env file.")

        session_name = input('\nEnter the session name (press Enter to exit): ')

        if not session_name:
            return None

        await self.add_to_json(session_name=session_name, proxy_chain=proxy_chain)

    async def add_to_json(self, session_name: str, proxy_chain: ProxyChain = None):
        device = await self.device_manager.get_user_device(session_name=session_name)

        if proxy_chain:
            raw_proxy = proxy_chain.get_next_proxy()
        elif self.skip_proxy_binding:
            raw_proxy = ""
        else:
            raw_proxy = input(
                "Input the proxy in the format type://user:pass@ip:port (press Enter to use without proxy): ")

        tg_client = await self.get_tg_client(session_name=session_name, proxy=raw_proxy, device=device)

        async with tg_client:
            await tg_client.start()
            user_data = await tg_client.get_me()

        dict_ = {
            "session_name": session_name,
            "proxy": raw_proxy if raw_proxy else "",
        }

        bindings_full_path = os.path.join(self.workdir, "bindings.json")
        save_to_json(path=bindings_full_path,
                     dict_=dict_)
        logger.success(f'Session added successfully @{user_data.username} |'
                       f' {user_data.first_name} {user_data.last_name}')

        return dict_

    @staticmethod
    async def get_tg_client(session_name: str,
                            proxy: str | None,
                            device: UniqueDevice):

        if not session_name:
            raise FileNotFoundError(f"Not found session {session_name}")

        if not settings.API_ID or not settings.API_HASH:
            raise ValueError("API_ID and API_HASH not found in the ..env file.")

        if proxy:
            proxy = Proxy.from_str(proxy=proxy)
        else:
            proxy = None

        proxy_dict = {
            "proxy_type": proxy.protocol,
            "username": proxy.login,
            "password": proxy.password,
            "addr": proxy.host,
            "port": proxy.port
        } if proxy else None

        session_path = "sessions/"
        session_path = os.path.join(session_path, session_name)

        client_params = {
            "api_id": settings.API_ID,
            "api_hash": settings.API_HASH,
            "session": session_path,
        }

        app_version = device.app_version
        client_params["app_version"] = app_version

        android_device = f'{device.manufacturer} {device.model}'
        client_params["device_model"] = android_device

        android_version = device.android.version
        client_params["system_version"] = f"Android {android_version}"

        if proxy_dict:
            client_params["proxy"] = proxy_dict

        tg_client = TelegramClient(**client_params)

        async with tg_client:
            await tg_client.start()

        return tg_client

