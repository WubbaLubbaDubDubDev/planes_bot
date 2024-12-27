[![Static Badge](https://img.shields.io/badge/Telegram-Bot%20Link-Link?style=for-the-badge&logo=Telegram&logoColor=white&logoSize=auto&color=blue)](https://t.me/plane_cryptobot/planes?startapp=ref_T78O2Z)

## PLANES FARMING BOT ( free version )

## Recommendation before use

## 🔥🔥 Use PYTHON 3.11 🔥🔥

This bot is built on my **new experimental framework** that ties unique device parameters to each session.  
⚠️ **Important Note**: Importing sessions from other software may lead to a **ban of your Telegram account**.  
To avoid this risk, it is highly recommended to register **new sessions** exclusively for this bot.  

## Features

| Feature                                        | Free Version | Paid Version |
|------------------------------------------------|:------------:|:------------:|
| Sending messages                               |      ✅       |      ✅       |
| Completing tasks                               |      ✅       |      ✅       |
| Automatic Ad Watching for Energy Recovery      |      ❌       |      ✅       |
| Night mode                                     |      ✅       |      ✅       |
| Proxy binding support                          |      ✅       |      ✅       |
| Using proxies without binding                  |      ✅       |      ✅       |
| Built with Telethon                            |      ✅       |      ✅       |
| Protection against API changes                 |      ❌       |      ✅       |
| Option to switch between Telethon and Pyrogram |      ❌       |      ✅       |
| Tracking farm profit via your Telegram bot     |      ❌       |      ✅       |
| All referrals become yours                     |      ❌       |      ✅       |







---

## Paid Version

The paid version is **currently under development**. Stay tuned for updates and announcements. 🚀

---

## Configuration

The bot uses a configuration file `.env` to manage parameters. Below is a list of all configurable options:

| Parameter                         | Description                                                                           |
|-----------------------------------|---------------------------------------------------------------------------------------|
| `API_ID`                          | Your Telegram API ID                                                                  |
| `API_HASH`                        | Your Telegram API hash                                                                |
| `START_DELAY`                     | Delay range (in seconds) before starting the bot. Example: `[120, 360]`.              |
| `ENABLE_TASKS`                    | Enable or disable task completion. Example: `True`.                                   |
| `TASKS_BLACKLIST`                 | List of tasks to ignore. Example: `["put ✈️  in your name", "boost planes channel"]`. |
| `ENABLE_MESSAGE_SENDING`          | Enable or disable message sending. Example: `True`.                                   |
| `REF_ID`                          | Referral ID for the bot. Example: `"T78O2Z"`.                                         |
| `NIGHT_MODE`                      | Enable or disable night mode. Example: `True`.                                        |
| `NIGHT_SLEEP_START_HOURS`         | Range of hours for night mode to start. Example: `[22, 2]`.                           |
| `NIGHT_SLEEP_DURATION`            | Range of sleep duration (in hours) during night mode. Example: `[6, 9]`.              |
| `SESSIONS_DIR`                    | Directory for session files. Example: `"sessions"`.                                   |
| `SESSIONS_STATE_DIR`              | Directory for session states. Example: `"sessions"`.                                  |
| `DEVICES_DIR`                     | Directory for device files. Example: `"sessions"`.                                    |
| `PROXIES_FILE`                    | Path to the proxies file. Example: `"bot/config/proxies.txt"`.                        |
| `USE_PROXY`                       | Enable or disable proxies. Example: `True`.                                           |
| `USE_PROXY_WITHOUT_BINDINGS`      | Use proxies without binding them to sessions. Example: `False`.                       |
| `AUTO_BIND_PROXIES`               | Automatically bind proxies to sessions. Example: `False`.                             |
| `SKIP_PROXY_BINDING`              | Skip proxy binding prompts for new sessions. Example: `False`.                        |
| `ALWAYS_ACCEPT_DEVICE_CREATION`   | Always accept device creation prompts. Example: `False`.                              |
| `ALWAYS_ACCEPT_BINDINGS_CREATION` | Always accept binding creation prompts. Example: `False`.                             |
| `SLEEP_TIME`                      | Range of sleep times (in seconds) between bot activities. Example: `[10800, 64800]`.  |

---

## Quick Start 📚

To quickly install libraries and run the bot - open `run.bat` on Windows or `run.sh` on Linux.

## Prerequisites
Before you begin, make sure you have the following installed:
- [Python](https://www.python.org/downloads/) **version 3.11**

## Obtaining API Keys
1. Go to my.telegram.org and log in using your phone number.
2. Select "API development tools" and fill out the form to register a new application.
3. Record the `API_ID` and `API_HASH` provided after registering your application in the `.env` file.

## Installation
You can download the [**repository**](https://github.com/WubbaLubbaDubDubDev/planes_bot) by cloning it to your system and installing the necessary dependencies:
git clone https://github.com/WubbaLubbaDubDubDev/planes_bot


Then you can do automatic installation by typing:

### Windows:
```shell
./run.bat
```

### Linux:
```shell
chmod +x run.sh
./run.sh
```

### Running in Docker

To run the project in Docker, navigate to the root directory of the script and execute the following command:
```shell
docker-compose up --build
```

## Linux manual installation
```shell
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
cp .env-example .env
nano .env  # Here you must specify your API_ID and API_HASH, the rest is taken by default
python3 main.py
# 1 - Run clicker
# 2 - Creates a session
# 3 = Quit
```

## Windows manual installation
```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env-example .env
# Here you must specify your API_ID and API_HASH, the rest is taken by default
python main.py
# 1 - Run clicker
# 2 - Creates a session
# 3 = Quit
```
