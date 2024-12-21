from TGDeviceGen.models.device import Device


class Manufacturer:
    def __init__(self, name: str):
        self.name = name
        self.devices = []

    def add_device(self, device: Device):
        self.devices.append(device)

