from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TeamRoster(Base):
    """Which team a player was on for a given season (season comes from
    team.season_id, not repeated here). One row per player per team."""

    __tablename__ = "team_rosters"
    __table_args__ = (UniqueConstraint("player_id", "team_id", name="uq_roster_player_team"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    jersey_number: Mapped[int | None]

    player: Mapped["Player"] = relationship(back_populates="rosters")
    team: Mapped["Team"] = relationship(back_populates="rosters")
