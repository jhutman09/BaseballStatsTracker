from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Season(Base):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)  # e.g. "2026 Spring"
    year: Mapped[int]
    start_date: Mapped[date | None]
    end_date: Mapped[date | None]

    rosters: Mapped[list["Roster"]] = relationship(back_populates="season")
