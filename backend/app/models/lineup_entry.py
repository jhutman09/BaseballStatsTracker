from sqlalchemy import CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class LineupEntry(Base):
    """One stretch of one player in one batting slot of one team's lineup for
    a game, as written on the scorecard. A substitute is a new row in the
    same slot with the inning they entered; a position change is a new row
    for the same player. inning_entered is NULL for a starter."""

    __tablename__ = "lineup_entries"
    __table_args__ = (
        CheckConstraint("batting_slot >= 1", name="ck_lineup_slot_positive"),
        CheckConstraint(
            "inning_entered IS NULL OR inning_entered >= 1", name="ck_lineup_inning_positive"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    roster_id: Mapped[int] = mapped_column(ForeignKey("rosters.id"))
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    batting_slot: Mapped[int]
    position: Mapped[str] = mapped_column(String(3))
    inning_entered: Mapped[int | None]

    game: Mapped["Game"] = relationship(back_populates="lineup_entries")
    roster: Mapped["Roster"] = relationship()
    player: Mapped["Player"] = relationship()
