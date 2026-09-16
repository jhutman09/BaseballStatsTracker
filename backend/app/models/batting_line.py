from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class BattingLine(Base):
    """One player's batting totals for one game, straight off the scorebook."""

    __tablename__ = "batting_lines"
    __table_args__ = (UniqueConstraint("game_id", "player_id", name="uq_batting_game_player"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    roster_id: Mapped[int] = mapped_column(ForeignKey("rosters.id"))  # which side they played for

    at_bats: Mapped[int] = mapped_column(default=0)
    runs: Mapped[int] = mapped_column(default=0)
    hits: Mapped[int] = mapped_column(default=0)
    doubles: Mapped[int] = mapped_column(default=0)
    triples: Mapped[int] = mapped_column(default=0)
    home_runs: Mapped[int] = mapped_column(default=0)
    rbi: Mapped[int] = mapped_column(default=0)
    walks: Mapped[int] = mapped_column(default=0)
    strikeouts: Mapped[int] = mapped_column(default=0)
    stolen_bases: Mapped[int] = mapped_column(default=0)

    game: Mapped["Game"] = relationship(back_populates="batting_lines")
    player: Mapped["Player"] = relationship()
    roster: Mapped["Roster"] = relationship()
