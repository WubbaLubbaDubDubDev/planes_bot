from dataclasses import dataclass


@dataclass
class Card:
    id: int
    media_url: str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(id=data["id"],
                   media_url=data["media_url"])
