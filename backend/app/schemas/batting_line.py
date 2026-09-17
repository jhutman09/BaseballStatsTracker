from pydantic import BaseModel, ConfigDict


class BattingLineBase(BaseModel):
    game_id: int
    player_id: int
    roster_id: int
    at_bats: int = 0
    runs: int = 0
    hits: int = 0
    doubles: int = 0
    triples: int = 0
    home_runs: int = 0
    rbi: int = 0
    walks: int = 0
    strikeouts: int = 0
    stolen_bases: int = 0


class BattingLineCreate(BattingLineBase):
    pass


class BattingLineRead(BattingLineBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BattingLineUpdate(BaseModel):
    game_id: int | None = None
    player_id: int | None = None
    roster_id: int | None = None
    at_bats: int | None = None
    runs: int | None = None
    hits: int | None = None
    doubles: int | None = None
    triples: int | None = None
    home_runs: int | None = None
    rbi: int | None = None
    walks: int | None = None
    strikeouts: int | None = None
    stolen_bases: int | None = None
