from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Player(Base):
    """A person, independent of any team/season, so one kid's career can span
    multiple years and teams without duplicating their identity each time."""

    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    notes: Mapped[str | None]

    roster_entries: Mapped[list["RosterEntry"]] = relationship(back_populates="player")
