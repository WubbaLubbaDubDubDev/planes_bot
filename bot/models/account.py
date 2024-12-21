from dataclasses import dataclass
from TGDeviceGen.models.unique_device import UniqueDevice


@dataclass
class Account:
    session_name: str
    proxy: str
    device: UniqueDevice

