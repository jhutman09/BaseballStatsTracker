from pydantic import BaseModel, ConfigDict


class ClubBase(BaseModel):
    name: str


class ClubCreate(ClubBase):
    pass


class ClubRead(ClubBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ClubUpdate(BaseModel):
    name: str | None = None
