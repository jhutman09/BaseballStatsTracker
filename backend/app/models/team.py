from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Team(Base):
    __tablename__ = "teams"
    __table_args__ = (UniqueConstraint("season_id", "name", name="uq_team_season_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"))
    name: Mapped[str] = mapped_column(String(100))

    season: Mapped["Season"] = relationship(back_populates="teams")
    rosters: Mapped[list["TeamRoster"]] = relationship(back_populates="team")
