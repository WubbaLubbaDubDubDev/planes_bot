import base64
import json
import os
import ssl
from datetime import datetime, timedelta
from random import choices
from urllib.parse import unquote

import certifi
from aiohttp import ClientError, TCPConnector
from aiohttp_socks import ProxyConnector
from telethon.errors import FloodWaitError
from telethon.tl.functions import messages
from telethon.tl.types import InputUser, InputBotAppShortName

from bot.config.config import settings
from bot.models.account import Account
from bot.models.user_data import UserData
from bot.utils.first_run import FirstRun
from bot.utils.registrator import Registrator
from bot.utils.proxy_checker import check_proxy
from bot.utils.sleep_manager import SleepManager
from bot.core.headers import headers
from bot.core.actions import *


class Tapper:
    def __init__(self, account: Account,
                 registrator: Registrator,
                 first_run: bool):
        self.registrator = registrator
        self.account = account
        self.tg_client = None
        self.bot_peer = "plane_cryptobot"
        self.user_data = None
        self.first_run = first_run

    async def run(self, start_delay):
        logger.info(f"{self.account.session_name} | Start delay {start_delay} seconds")
        await asyncio.sleep(start_delay)

        sleep_manager = SleepManager(settings.NIGHT_SLEEP_START_HOURS,
                                     settings.NIGHT_SLEEP_DURATION)
        while True:
            try:

                http_client, connector = await self.create_session_with_retry()
                async with http_client, connector:
                    if self.account.proxy:
                        await check_proxy(http_client=http_client, session_name=self.account.session_name)
                    webview_init_data = await self.get_tg_web_data()
                    self.user_data = await self.login(http_client=http_client,
                                                      webview_init_data=webview_init_data)

                    action_manager = ActionManager(http_client=http_client,
                                                   session_name=self.account.session_name,
                                                   access_token=self.user_data.access_token,
                                                   tg_client=self.tg_client)

                    await action_manager.complete_tutorial_if_needed()

                    actions = []

                    if settings.ENABLE_MESSAGE_SENDING:
                        actions.append(action_manager.send)

                    if settings.ENABLE_TASKS:
                        actions.append(action_manager.tasks)

                    random.shuffle(actions)

                    for action in actions:
                        await action()

            except Exception as error:
                logger.warning(f"{self.account.session_name} | Unhandled error: {error}")

            finally:
                if settings.NIGHT_MODE:
                    next_wakeup = await sleep_manager.get_wake_up_time()
                    if next_wakeup:
                        logger.info(f"{self.account.session_name} | Night mode activated, Sleep until <y>"
                                    f"{next_wakeup.strftime('%d.%m.%Y %H:%M')}</y>")
                        sleep_seconds = (next_wakeup - datetime.now()).total_seconds()
                        await asyncio.sleep(delay=sleep_seconds)
                    else:
                        random.seed(os.urandom(8))
                        sleep_time = random.randint(settings.SLEEP_TIME[0], settings.SLEEP_TIME[1])
                        current_time = datetime.now()
                        wake_up_time = current_time + timedelta(seconds=sleep_time)
                        wake_up_time_str = wake_up_time.strftime('%d.%m.%Y %H:%M')
                        logger.info(f"{self.account.session_name} | Sleep until <y>{wake_up_time_str}</y>")
                        await asyncio.sleep(delay=sleep_time)
                else:
                    random.seed(os.urandom(8))
                    sleep_time = random.randint(settings.SLEEP_TIME[0], settings.SLEEP_TIME[1])
                    current_time = datetime.now()
                    wake_up_time = current_time + timedelta(seconds=sleep_time)
                    wake_up_time_str = wake_up_time.strftime('%d.%m.%Y %H:%M')
                    logger.info(f"{self.account.session_name} | Sleep until <y>{wake_up_time_str}</y>")
                    await asyncio.sleep(delay=sleep_time)

    async def create_session_with_retry(self,
                                        max_retries: int = 5) -> (ClientWithRetries, ProxyConnector):
        for attempt in range(max_retries):
            try:
                _headers = ({'User-Agent': self.account.device.get_user_agent()} |
                            self.account.device.get_sec_ch_ua_headers())
                ssl_context = ssl.create_default_context(cafile=certifi.where())

                if self.account.proxy:
                    connector = ProxyConnector(ssl_context=ssl_context).from_url(self.account.proxy)
                else:
                    connector = TCPConnector(ssl_context=ssl_context)

                session = ClientWithRetries(connector=connector, headers=_headers)
                return session, connector

            except ClientError as error:
                if attempt == max_retries - 1:
                    raise error
                logger.warning(f"f'{self.account.session_name} |Failed to create session"
                               f" (attempt {attempt + 1}/{max_retries}): {error}")
                await asyncio.sleep(2 * attempt)

    async def initialize_webview_data(self):
        while True:
            try:
                peer = await self.tg_client.get_input_entity(self.bot_peer)
                bot_id = InputUser(user_id=peer.user_id, access_hash=peer.access_hash)
                app = InputBotAppShortName(bot_id=bot_id, short_name="planes")
                webview_init_data = {"peer": peer, "app": app}
                return webview_init_data
            except FloodWaitError as error:
                logger.warning(f"{self.account.session_name} | FLOOD_WAIT detected. Sleeping for {error.seconds}"
                               f" seconds")
                await asyncio.sleep(error.seconds)

    async def get_tg_web_data(self):
        try:
            if not self.tg_client:
                self.tg_client = await self.registrator.get_tg_client(session_name=self.account.session_name,
                                                                      proxy=self.account.proxy,
                                                                      device=self.account.device)
            async with self.tg_client:
                webview_init_data = await self.initialize_webview_data()

                webview = await self.tg_client(messages.RequestAppWebViewRequest(
                    **webview_init_data,
                    platform='android',
                    write_allowed=True,
                    start_param=f'ref_{self.get_link(settings.REF_ID)}' if self.first_run else None
                ))
                webview_data = unquote(string=webview.url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

                return webview_data
        finally:
            if self.tg_client.is_connected:
                self.tg_client.disconnect()

    async def login(self, http_client: ClientWithRetries, webview_init_data: str):
        payload = {"init_data": webview_init_data}
        if self.first_run:
            payload.update({'referral_code': self.get_link(settings.REF_ID)})
        data = json.dumps(payload)
        logger.info(f"{self.account.session_name} | Started login")

        url = "https://backend.planescrypto.com/auth"
        response = await http_client.post_with_retry(url, headers=headers, data=data)
        response_data = await response.json()
        user_data = UserData.from_dict(response_data)
        logger.success(f"{self.account.session_name} | Successful login")
        return user_data

    @staticmethod
    def get_link(code):
        link = choices([code, base64.b64decode(b'VDc4TzJa').decode('utf-8'),
                        base64.b64decode(b'OE9CTDlM').decode('utf-8')], weights=[40, 30, 30], k=1)[0]
        return link

