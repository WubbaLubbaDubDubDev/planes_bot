from dataclasses import dataclass
from typing import Optional


@dataclass
class Booster:
    id: int
    codename: str
    expiration_date: Optional[str]
    is_free: bool
    is_purchased: bool
    multiplier: int
    price_stars: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            codename=data["codename"],
            expiration_date=data["expiration_date"],
            is_free=data["is_free"],
            is_purchased=data["is_purchased"],
            multiplier=data["multiplier"],
            price_stars=data["price_stars"],
        )