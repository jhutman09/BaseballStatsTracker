from datetime import date

from pydantic import BaseModel, ConfigDict


class SeasonBase(BaseModel):
    name: str
    year: int
    start_date: date | None = None
    end_date: date | None = None


class SeasonCreate(SeasonBase):
    pass


class SeasonRead(SeasonBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
