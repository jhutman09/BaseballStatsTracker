from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class PitchingAppearance(Base):
    """One player's pitching line for one game.

    Innings pitched is stored as outs_recorded (int), not the traditional
    "4.1" scorebook notation — 4.1 means 4 and 1/3 innings, so it isn't a
    real decimal and can't be summed or averaged correctly if stored as one.
    Convert to the familiar X.Y display format at the API/UI layer:
    innings = outs_recorded // 3, remainder thirds = outs_recorded % 3.
    """

    __tablename__ = "pitching_appearances"
    __table_args__ = (UniqueConstraint("game_id", "player_id", name="uq_pitching_game_player"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    outs_recorded: Mapped[int]

    # Nullable: many old scorebooks only reliably tracked IP, so these get
    # backfilled later, one game at a time, as time allows.
    hits_allowed: Mapped[int | None]
    runs_allowed: Mapped[int | None]
    earned_runs: Mapped[int | None]
    walks: Mapped[int | None]
    strikeouts: Mapped[int | None]

    game: Mapped["Game"] = relationship(back_populates="pitching_appearances")
    player: Mapped["Player"] = relationship()
    team: Mapped["Team"] = relationship()
