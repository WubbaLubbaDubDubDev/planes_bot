from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    START_DELAY: list = [120, 360]
    SLEEP_TIME: list[int] = [10800, 64800]
    ENABLE_TASKS: bool = True
    TASKS_BLACKLIST: list[str] = ["put ✈️  in your name", "boost planes channel", "explore Telegram Apps"]
    ENABLE_MESSAGE_SENDING: bool = True
    REF_ID: str = "T78O2Z"

    NIGHT_MODE: bool = True
    NIGHT_SLEEP_START_HOURS: list[int] = [22, 2]
    NIGHT_SLEEP_DURATION: list[int] = [4, 8]

    SESSIONS_DIR: str = "sessions"
    SESSIONS_STATE_DIR: str = "sessions"
    DEVICES_DIR: str = "sessions"

    PROXIES_FILE: str = "bot/config/proxies.txt"
    USE_PROXY: bool = True  # If you want to use proxies (linked to a specific session)

    USE_PROXY_WITHOUT_BINDINGS: bool = False  # If you do not want to use binding (a proxy is fetched from
    # the proxy file for each session during every run)
    AUTO_BIND_PROXIES: bool = False  # If you want to automatically bind a proxy to each session
    SKIP_PROXY_BINDING: bool = False  # If you do not want to use proxies and do not want
    # to see a prompt to bind a proxy when creating a new session
    ALWAYS_ACCEPT_DEVICE_CREATION: bool = False
    ALWAYS_ACCEPT_BINDINGS_CREATION: bool = False


settings = Settings()
