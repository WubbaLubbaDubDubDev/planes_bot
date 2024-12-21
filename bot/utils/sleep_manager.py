import os
import random
from datetime import datetime, timedelta


class SleepManager:
    def __init__(self, sleep_start_range: list, sleep_duration_range: list):
        self.sleep_start_range = sleep_start_range
        self.sleep_duration_range = sleep_duration_range

    async def __should_sleep(self):
        current_hour = datetime.now().hour
        start_hour, end_hour = self.sleep_start_range

        if start_hour > end_hour:
            return current_hour >= start_hour or current_hour < end_hour
        else:
            return start_hour <= current_hour < end_hour

    async def get_wake_up_time(self):
        if not (await self.__should_sleep()):
            return None

        random.seed(os.urandom(8))
        sleep_duration = random.uniform(*self.sleep_duration_range)
        sleep_end_time = datetime.now() + timedelta(hours=sleep_duration)
        return sleep_end_time
