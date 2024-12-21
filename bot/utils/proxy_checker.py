import aiohttp

from bot.utils.client_with_retries import ClientWithRetries
from bot.utils.logger import logger


async def check_proxy(http_client: ClientWithRetries, session_name: str) -> None:
    timeout = aiohttp.ClientTimeout(total=10)

    try:
        async with ClientWithRetries(timeout=timeout) as client_without_proxy:
            real_response = await client_without_proxy.get_with_retry(
                url='https://httpbin.org/ip',
                ssl=False
            )
            real_response.raise_for_status()
            real_data = await real_response.json()
            real_ip = real_data.get('origin')
            logger.info(f"{session_name} | Real IP: {real_ip}")
    except Exception as error:
        raise RuntimeError(f"{session_name} | Failed to fetch real IP: {error}")

    try:
        proxy_response = await http_client.get(url='https://httpbin.org/ip', ssl=False, timeout=timeout)
        proxy_response.raise_for_status()
        data = await proxy_response.json()
        ip = data.get('origin')
        logger.info(f"{session_name} | Proxy IP: {ip}")
        return

    except Exception as error:
        raise RuntimeError(f"{session_name} | Invalid proxy: {error}")
