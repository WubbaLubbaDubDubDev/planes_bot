import asyncio
import copy
import random

from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import ChannelsTooMuchError, ChannelInvalidError, ChannelPrivateError, InviteRequestSentError

from bot.config.config import settings
from bot.core.headers import send_headers
from bot.utils.client_with_retries import ClientWithRetries
from bot.utils.logger import logger
from bot.models.profile import Profile


class ActionManager:
    def __init__(self, http_client: ClientWithRetries,
                 session_name: str,
                 tg_client: TelegramClient,
                 access_token: str):
        self.http_client = http_client
        self.session_name = session_name
        self.access_token = access_token
        auth_header = {'Authorization': f'Bearer {self.access_token}'}
        self.response_header = copy.deepcopy(send_headers)
        self.response_header.update(auth_header)
        self.tg_client = tg_client

    async def subscribe_channel(self, channel):
        async with self.tg_client:
            await self.tg_client(JoinChannelRequest(channel=channel))

    async def tutorial_is_completed(self):
        url = 'https://backend.planescrypto.com/user/tutorial-status'
        response = await self.http_client.get_with_retry(url=url, headers=self.response_header)
        return (await response.json())['is_tutorial_completed']

    async def complete_tutorial_if_needed(self):
        if not (await self.tutorial_is_completed()):
            await self.tutorial_is_completed()
            url = 'https://backend.planescrypto.com/user/complete-tutorial'
            await self.http_client.post_with_retry(url=url, headers=self.response_header, json={})
            logger.info(f'{self.session_name} | The tutorial has been completed')
        else:
            logger.info(f'{self.session_name} | The tutorial has been completed earlier')

    async def send(self):
        profile = await self.get_profile()

        earned_total = 0

        if profile.available_messages_count <= 0:
            # logger.info(f'{self.session_name} | No available messages to send. The next message will be available on:'
            #            f' <y>{profile.next_available_message_date.strftime("%d.%m.%Y %H:%M")}</y>')
            pass

        else:
            for _ in range(profile.available_messages_count):
                url = 'https://backend.planescrypto.com/planes/success-share-message'
                response = await self.http_client.post_with_retry(url=url,
                                                                  headers=self.response_header,
                                                                  json={})
                response_data = await response.json()
                earned_amount = response_data["earned_amount"]
                earned_total += earned_amount
                logger.success(f'{self.session_name} | Successfully sent the message. | Reward: <y>{earned_amount}</y>')
                delay = random.uniform(2.0, 5.0)
                await asyncio.sleep(delay)

            logger.info(f'{self.session_name} | That`s all for now. Total earned for the session: <y>{earned_total}</y>')

    async def get_profile(self):
        url = 'https://backend.planescrypto.com/user/profile'
        response = await self.http_client.get_with_retry(url=url,
                                                         headers=self.response_header)
        response_data = await response.json()
        profile = Profile.from_dict(response_data)
        return profile

    async def tasks(self):
        available_tasks = await self.get_available_tasks()
        delay = random.uniform(2.0, 5.0)
        await asyncio.sleep(delay=delay)
        for task in available_tasks:
            task_title = task['task']['title']
            if task_title in settings.TASKS_BLACKLIST:
                continue
            task_id = task['task']['id']
            task_type = task['task']['task_type']
            award = task['task']['award']
            completed_task = False
            if task_type == 'telegram_story':
                completed_task = True
            elif task_type == 'null':
                completed_task = True
            elif task_type == 'referrals_count':
                referrals_count_needed = task['task']['additional_info']['special']
                referrals_data = await self.get_referrals()
                delay = random.uniform(2.0, 5.0)
                await asyncio.sleep(delay=delay)
                referrals_has = referrals_data['total_referrals']
                if int(referrals_count_needed) <= int(referrals_has):
                    completed_task = True
            elif task_type == 'telegram_boost':
                completed_task = False
            elif task_type == 'telegram_emoji_nick':
                completed_task = False
            elif task_type == 'telegram_subscribe':
                try:
                    channel_username = (task['task']['additional_info']['link_button_url']).split("/")[-1]
                    await self.subscribe_channel(channel=channel_username)
                    completed_task = True
                except ChannelsTooMuchError:
                    logger.warning(f'{self.session_name} | You have joined too many channels/supergroups.')
                except ChannelInvalidError:
                    logger.warning(f'{self.session_name} | Invalid channel object.')
                except ChannelPrivateError:
                    logger.warning(
                        f'{self.session_name} | The channel specified is private and you lack permission to'
                        f' access it. Another reason may be that you were banned from it.')
                except InviteRequestSentError:
                    completed_task = True
                    logger.warning(f'{self.session_name} | You have successfully requested to join this chat or'
                                   f' channel.')
            if completed_task:
                delay = random.uniform(10.0, 15.0)
                await asyncio.sleep(delay=delay)
                succeeded_status = await self.check_task_status(task_id=task_id)
                if succeeded_status:
                    logger.success(f'{self.session_name} | Successfully completed task: <y>"{task_title}"</y> | '
                                   f'Reward: <y>{award}</y>')
                else:
                    logger.warning(f'{self.session_name} | Failed to complete task: <y>"{task_title}"</y>')
            else:
                logger.info(f'{self.session_name} | Cannot complete task: <y>"{task_title}"</y> yet,'
                            f' as the requirements are not met')

    async def get_available_tasks(self):
        url = f'https://backend.planescrypto.com/tasks'
        response = await self.http_client.get_with_retry(url=url,
                                                         headers=self.response_header)
        response_data = await response.json()
        filtered_tasks = [
            task for task in response_data["tasks"]
            if task["status"] == "idle" and not task["task"]["is_disabled"]
        ]
        return filtered_tasks

    async def check_task_status(self, task_id: int):
        url = f'https://backend.planescrypto.com/tasks/check/{task_id}'
        response = await self.http_client.post_with_retry(url=url,
                                                          headers=self.response_header,
                                                          json={})
        response_data = await response.json()
        status = True if (response_data["status"] == "succeeded") else False
        return status

    async def get_referrals(self):
        url = 'https://backend.planescrypto.com/user-referral/all?page=1&page_size=10'
        response = await self.http_client.get_with_retry(url=url,
                                                         headers=self.response_header)
        response_data = await response.json()
        return response_data
