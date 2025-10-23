from pydantic import BaseModel


class Sector(BaseModel):
    max: int | None = None
    min: int | None = None
    points: list[list[str]]


class Airspace(BaseModel):
    id: str
    group: str
    uid: str
    owner: list[str]
    sectors: list[Sector]
