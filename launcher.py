import argparse
import asyncio
from random import randint

from bot.config.config import settings
from bot.core.tapper import Tapper
from bot.utils.device_manager import DeviceManager
from bot.utils.logger import logger
from bot.utils.proxy_chain import ProxyChain
from bot.utils.registrator import Registrator
from bot.utils.first_run import FirstRun
from bot.core.accounting import Accounts

art_splash = '''

    //   ) )     / /        // | |     /|    / /     //   / /     //   ) )
   //___/ /     / /        //__| |    //|   / /     //____       ((
  / ____ /     / /        / ___  |   // |  / /     / ____          \\
 //           / /        //    | |  //  | / /     //                 ) )
//           / /____/ / //     | | //   |/ /     //____/ /    ((___ / /                                             
'''
author = "by WubbaLubbaDubDubDev"

menu_items = """                                             
Select an action:

    1. Run bot
    2. Create session
    3. Quit

"""


async def process() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=int, help="Action to perform")
    parser.add_argument("-d", "--docker", action="store_true", help="Run in Docker mode")
    args = parser.parse_args()

    proxy_chain = None

    if settings.USE_PROXY or settings.USE_PROXY_WITHOUT_BINDINGS:
        proxy_chain = ProxyChain(sessions_workdir=settings.SESSIONS_DIR,
                                 proxies_file=settings.PROXIES_FILE)
    device_manager = DeviceManager(workdir=settings.SESSIONS_DIR)
    registrator = Registrator(workdir=settings.SESSIONS_DIR,
                              device_manager=device_manager,
                              api_id=settings.API_ID,
                              api_hash=settings.API_HASH,
                              skip_proxy_binding=settings.SKIP_PROXY_BINDING)

    action = args.action
    if not action:
        print('\033[97m' + '\033[97m' + art_splash + '\033[97m')
        print('\033[1m' + '\033[93m' + author + '\033[0m')

    while True:
        if not args.docker:
            print(menu_items)

            while True:
                action = input("> ")

                if not action.isdigit():
                    logger.warning("Action must be number")
                elif action not in ["1", "2", "3"]:
                    logger.warning("Action must be 1, 2 or 3")
                else:
                    action = int(action)
                    break
        else:
            print("\nRunning in Docker mode!\n")
            action = 1

        if action == 1:
            await run(registrator=registrator,
                      device_manager=device_manager,
                      proxy_chain=proxy_chain,
                      docker=args.docker)

        elif action == 2:
            await register_session(registrator=registrator,
                                   proxy_chain=proxy_chain)

            while True:
                repeat = input("Do you want to register another session? (y/n): ").strip().lower()
                if repeat == 'y':
                    break
                elif repeat == 'n':
                    return
                elif repeat not in ['y', 'n']:
                    print("Invalid choice. Please enter 'y' or 'n'.")

        elif action == 3:
            print("Goodbye!")
            return


async def run(registrator: Registrator,
              device_manager: DeviceManager,
              proxy_chain: ProxyChain,
              docker: bool):
    accounts_mngr = Accounts(workdir=settings.SESSIONS_DIR,
                             registrator=registrator,
                             device_manager=device_manager,
                             accept_bindings_creation=True if docker else settings.ALWAYS_ACCEPT_BINDINGS_CREATION,
                             accept_device_creation=True if docker else settings.ALWAYS_ACCEPT_DEVICE_CREATION,
                             use_proxy=settings.USE_PROXY or settings.USE_PROXY_WITHOUT_BINDINGS)
    tasks = []
    proxy_chain_without_bindings = ProxyChain(proxies_file=settings.PROXIES_FILE,
                                              sessions_workdir=settings.SESSIONS_DIR,
                                              load_proxies_from_json=False)
    delay_between_account = 0
    for account in await accounts_mngr.get_accounts(proxy_chain=proxy_chain):
        if settings.USE_PROXY_WITHOUT_BINDINGS:
            account.proxy = proxy_chain_without_bindings.get_next_proxy()

        first_run = FirstRun(sessions_dir=settings.SESSIONS_STATE_DIR).check_session(account.session_name)

        tapper = Tapper(account=account,
                        registrator=registrator,
                        first_run=first_run)
        tasks.append(tapper.run(start_delay=delay_between_account))
        delay_between_account = randint(settings.START_DELAY[0], settings.START_DELAY[1])

    await asyncio.gather(*tasks)


async def register_session(registrator: Registrator,
                           proxy_chain: ProxyChain = None):
    if settings.AUTO_BIND_PROXIES:
        await registrator.register_session(proxy_chain=proxy_chain)
    else:
        await registrator.register_session()
