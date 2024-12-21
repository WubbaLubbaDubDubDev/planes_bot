from dataclasses import dataclass
from datetime import datetime


@dataclass
class Profile:
    available_messages_count: int
    balance: int
    first_name: str
    last_name: str
    next_available_message_date: datetime
    photo_url: str
    referral_url: str
    telegram_id: str
    username: str

    @classmethod
    def from_dict(cls, data: dict):
        next_message_date = data.get("next_available_message_date")
        next_available_message_date = (
            datetime.fromisoformat(next_message_date.rstrip('Z'))
            if next_message_date
            else None
        )
        return cls(
            available_messages_count=data.get("available_messages_count", 0),
            balance=data.get("balance", 0),
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            next_available_message_date=next_available_message_date,
            photo_url=data.get("photo_url", ""),
            referral_url=data.get("referral_url", ""),
            telegram_id=data.get("telegram_id", ""),
            username=data.get("username", "")
        )