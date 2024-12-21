import os

from bot.utils.file_manager import load_from_json
from bot.utils.logger import logger
from bot.utils.proxy_chain import ProxyChain
from bot.utils.registrator import Registrator
from bot.models.account import Account
from bot.utils.device_manager import DeviceManager


class Accounts:
    def __init__(self, workdir: str,
                 registrator: Registrator,
                 device_manager: DeviceManager,
                 accept_bindings_creation: bool,
                 accept_device_creation: bool,
                 use_proxy: bool):
        self.workdir = workdir
        self.registrator = registrator
        self.device_manager = device_manager
        self.accept_bindings_creation = accept_bindings_creation
        self.accept_device_creation = accept_device_creation
        self.use_proxy = use_proxy

    async def __get_available_accounts(self, sessions: list, proxy_chain: ProxyChain = None):
        bindings_full_path = os.path.join(self.workdir, "bindings.json")
        accounts_from_json = load_from_json(bindings_full_path)
        available_accounts = []

        for session in sessions:
            saved_account = await self.__find_account(accounts_from_json, session)

            if not saved_account:
                add_to_json = False

                if self.accept_bindings_creation:
                    add_to_json = True
                else:
                    logger.warning(f'{session}.session does not exist in {bindings_full_path}')
                    if await self.__confirm_action(f"Add {session} to bindings.json? (y/n): "):
                        add_to_json = True

                if add_to_json:
                    saved_account = await self.registrator.add_to_json(session_name=session, proxy_chain=proxy_chain)

            if saved_account:
                if not await self.device_manager.is_exists(session_name=session):
                    logger.warning(f'{session}.device does not exist in {bindings_full_path}')
                    create_deice = False
                    if self.accept_device_creation:
                        create_deice = True
                    if await self.__confirm_action(f"Generate unique device for {session}? (y/n): "):
                        create_deice = True
                    if not create_deice:
                        break
                device = await self.device_manager.get_user_device(session)
                account = Account(session_name=session,
                                  proxy=saved_account['proxy'] if self.use_proxy else None,
                                  device=device)
                available_accounts.append(account)

        if not available_accounts:
            raise ValueError("Can't run script | Please add session(s) first.")

        return available_accounts

    @staticmethod
    async def __find_account(accounts_from_json, session):
        for account in accounts_from_json:
            if account['session_name'] == session:
                return account
        return None

    @staticmethod
    async def __confirm_action(message: str) -> bool:
        while True:
            ans = input(message).strip().lower()
            if ans in {'y', 'n'}:
                return ans == 'y'
            print("Invalid input. Please enter 'y' or 'n'.")

    async def __pars_sessions(self):
        sessions = []
        for file in os.listdir(self.workdir):
            if file.endswith(".session"):
                sessions.append(file.replace(".session", ""))
        return sessions

    async def get_accounts(self, proxy_chain: ProxyChain = None):
        sessions = await self.__pars_sessions()
        available_accounts = await self.__get_available_accounts(sessions, proxy_chain=proxy_chain)
        if not available_accounts:
            raise ValueError("Available sessions not found! Please, registrate session(s) first!")
        else:
            logger.success(f"Available sessions: {len(available_accounts)}.")

        return available_accounts
