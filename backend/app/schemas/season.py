from datetime import date

from pydantic import BaseModel, ConfigDict


class SeasonBase(BaseModel):
    name: str
    year: int
    start_date: date | None = None
    end_date: date | None = None


class SeasonCreate(SeasonBase):
    # Usually just inherits SeasonBase as-is: nothing extra is needed here
    # since the client provides everything up front when creating a season.
    pass


class SeasonRead(SeasonBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SeasonUpdate(BaseModel):
    name: str | None = None
    year: int | None = None
    start_date: date | None = None
    end_date: date | None = None
