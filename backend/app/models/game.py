from datetime import date

from sqlalchemy import CheckConstraint, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Game(Base):
    __tablename__ = "games"
    __table_args__ = (
        CheckConstraint("home_roster_id != away_roster_id", name="ck_game_rosters_differ"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    # No season_id column here: a game's season is derived through its
    # rosters (roster.season_id), so it's one fact in one place instead of
    # two that could drift out of sync.
    home_roster_id: Mapped[int] = mapped_column(ForeignKey("rosters.id"))
    away_roster_id: Mapped[int] = mapped_column(ForeignKey("rosters.id"))
    game_date: Mapped[date]
    field: Mapped[str | None] = mapped_column(String(100))
    home_score: Mapped[int | None]
    away_score: Mapped[int | None]
    notes: Mapped[str | None] = mapped_column(Text)

    home_roster: Mapped["Roster"] = relationship(foreign_keys=[home_roster_id])
    away_roster: Mapped["Roster"] = relationship(foreign_keys=[away_roster_id])
    batting_lines: Mapped[list["BattingLine"]] = relationship(back_populates="game")
    pitching_appearances: Mapped[list["PitchingAppearance"]] = relationship(back_populates="game")
