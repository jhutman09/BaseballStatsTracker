from pydantic import BaseModel, ConfigDict


class PlayerBase(BaseModel):
    first_name: str
    last_name: str
    notes: str | None = None


class PlayerCreate(PlayerBase):
    pass


class PlayerRead(PlayerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PlayerUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    notes: str | None = None
