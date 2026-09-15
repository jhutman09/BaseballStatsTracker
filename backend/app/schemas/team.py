from pydantic import BaseModel, ConfigDict


class TeamBase(BaseModel):
    season_id: int
    club_id: int
    name: str


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TeamUpdate(BaseModel):
    season_id: int | None = None
    club_id: int | None = None
    name: str | None = None
