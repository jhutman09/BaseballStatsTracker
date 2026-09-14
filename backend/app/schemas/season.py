from datetime import date

from pydantic import BaseModel, ConfigDict


class SeasonBase(BaseModel):
    # TODO: declare the fields a client can set when creating/reading a
    # season. Match the Season SQLAlchemy model's columns:
    #   name: str
    #   year: int
    #   start_date: date | None = None
    #   end_date: date | None = None
    pass


class SeasonCreate(SeasonBase):
    # Usually just inherits SeasonBase as-is: nothing extra is needed here
    # since the client provides everything up front when creating a season.
    pass


class SeasonRead(SeasonBase):
    # TODO: add the one field that only exists once a season is saved:
    #   id: int
    # The database assigns this — it's never something a client sends on
    # create, which is why it lives on SeasonRead but not SeasonBase.
    #
    # Also set:
    #   model_config = ConfigDict(from_attributes=True)
    # This tells Pydantic it's allowed to build this schema by reading
    # attributes off a SQLAlchemy Season object (season.id, season.name, ...)
    # instead of requiring a plain dict.
    pass
