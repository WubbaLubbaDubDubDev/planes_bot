import asyncio
from typing import Callable

import aiohttp


class ClientWithRetries(aiohttp.ClientSession):
    def __init__(self,
                 base_delay: int = 2,
                 max_retries: int = 5,
                 **kwargs):
        super().__init__(**kwargs)
        self.base_delay = base_delay
        self.max_retries = max_retries

    async def post_with_retry(self,
                              url: str,
                              base_delay: int = None,
                              max_retries: int = None,
                              **kwargs):
        return await self.__make_with_retries(
            lambda: super(ClientWithRetries, self).post(url=url, **kwargs),
            base_delay=base_delay,
            max_retries=max_retries
        )

    async def put_with_retry(self,
                             url: str,
                             base_delay: int = None,
                             max_retries: int = None,
                             **kwargs):
        return await self.__make_with_retries(
            lambda: super(ClientWithRetries, self).put(url=url, **kwargs),
            base_delay=base_delay,
            max_retries=max_retries
        )

    async def get_with_retry(self,
                             url: str,
                             base_delay: int = None,
                             max_retries: int = None,
                             **kwargs):
        return await self.__make_with_retries(
            lambda: super(ClientWithRetries, self).get(url=url, **kwargs),
            base_delay=base_delay,
            max_retries=max_retries
        )

    async def delete_with_retry(self,
                                url: str,
                                base_delay: int = None,
                                max_retries: int = None,
                                **kwargs):
        return await self.__make_with_retries(
            lambda: super(ClientWithRetries, self).delete(url=url, **kwargs),
            base_delay=base_delay,
            max_retries=max_retries
        )

    async def __make_with_retries(self,
                                  request_func: Callable,
                                  base_delay: int = None,
                                  max_retries: int = None,
                                  ):
        base_delay = base_delay if base_delay else self.base_delay
        max_retries = max_retries if max_retries else self.max_retries
        for attempt in range(max_retries):
            retry_delay = base_delay * (attempt + 1)
            try:
                response = await request_func()
                if 500 <= response.status < 600:
                    await asyncio.sleep(retry_delay)
                    continue
                response.raise_for_status()
                return response
            except aiohttp.ClientResponseError as error:
                status_code = error.status
                if 400 <= status_code < 500:
                    raise error
                raise error
        raise RuntimeError(f"Failed to make the request after {max_retries} attempts.")
