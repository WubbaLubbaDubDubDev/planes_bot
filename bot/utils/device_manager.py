import os
from TGDeviceGen.device_generator import Generator


class DeviceManager:
    def __init__(self, workdir):
        self.workdir = workdir

    async def get_user_device(self, session_name: str):
        device_file_name = f'{session_name}.device'
        device_file_full_name = os.path.join(self.workdir, device_file_name)
        generator = Generator()
        if await self.is_exists(session_name=session_name):
            device = generator.load(file_path=device_file_full_name)
        else:
            device = await self.generate_device(session_name=session_name)

        return device

    async def is_exists(self, session_name: str):
        file_names = [file for file in os.listdir(self.workdir) if os.path.isfile(os.path.join(self.workdir, file))]
        device_file_name = f'{session_name}.device'

        if device_file_name in file_names:
            return True
        else:
            return False

    async def generate_device(self, session_name: str):
        device_file_name = f'{session_name}.device'
        device_file_full_name = os.path.join(self.workdir, device_file_name)
        generator = Generator()
        device = generator.generate_unique_device()
        generator.save_device(file_path=device_file_full_name,
                              unique_device=device)
        return device

