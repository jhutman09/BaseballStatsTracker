from pydantic import BaseModel, ConfigDict


class RosterBase(BaseModel):
    season_id: int
    club_id: int
    name: str


class RosterCreate(RosterBase):
    pass


class RosterRead(RosterBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RosterUpdate(BaseModel):
    season_id: int | None = None
    club_id: int | None = None
    name: str | None = None
