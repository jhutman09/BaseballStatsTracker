from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class RosterEntry(Base):
    """Which roster (a club's roster for one season) a player belongs to.
    One row per player per roster."""

    __tablename__ = "roster_entries"
    __table_args__ = (UniqueConstraint("player_id", "roster_id", name="uq_roster_entry_player_roster"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    roster_id: Mapped[int] = mapped_column(ForeignKey("rosters.id"))
    jersey_number: Mapped[int | None]

    player: Mapped["Player"] = relationship(back_populates="roster_entries")
    roster: Mapped["Roster"] = relationship(back_populates="entries")
