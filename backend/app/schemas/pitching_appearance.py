from pydantic import BaseModel, ConfigDict


class PitchingAppearanceBase(BaseModel):
    game_id: int
    player_id: int
    roster_id: int
    outs_recorded: int
    hits_allowed: int | None = None
    runs_allowed: int | None = None
    earned_runs: int | None = None
    walks: int | None = None
    strikeouts: int | None = None


class PitchingAppearanceCreate(PitchingAppearanceBase):
    pass


class PitchingAppearanceRead(PitchingAppearanceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PitchingAppearanceUpdate(BaseModel):
    game_id: int | None = None
    player_id: int | None = None
    roster_id: int | None = None
    outs_recorded: int | None = None
    hits_allowed: int | None = None
    runs_allowed: int | None = None
    earned_runs: int | None = None
    walks: int | None = None
    strikeouts: int | None = None
