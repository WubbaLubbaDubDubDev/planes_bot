from dataclasses import dataclass


@dataclass
class UserData:
    access_token: str
    is_first_auth: bool
    start_bonus: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            access_token=data.get("access_token", None),
            is_first_auth=data.get("is_first_auth", None),
            start_bonus=data.get("start_bonus", None),
        )
