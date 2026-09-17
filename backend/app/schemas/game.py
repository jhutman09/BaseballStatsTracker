from datetime import date

from pydantic import BaseModel, ConfigDict


class GameBase(BaseModel):
    home_roster_id: int
    away_roster_id: int
    game_date: date
    field: str | None = None
    home_score: int | None = None
    away_score: int | None = None
    notes: str | None = None


class GameCreate(GameBase):
    pass


class GameRead(GameBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GameUpdate(BaseModel):
    home_roster_id: int | None = None
    away_roster_id: int | None = None
    game_date: date | None = None
    field: str | None = None
    home_score: int | None = None
    away_score: int | None = None
    notes: str | None = None
