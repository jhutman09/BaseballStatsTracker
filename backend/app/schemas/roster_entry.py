from pydantic import BaseModel, ConfigDict


class RosterEntryBase(BaseModel):
    player_id: int
    roster_id: int
    jersey_number: int | None = None


class RosterEntryCreate(RosterEntryBase):
    pass


class RosterEntryRead(RosterEntryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RosterEntryUpdate(BaseModel):
    player_id: int | None = None
    roster_id: int | None = None
    jersey_number: int | None = None
