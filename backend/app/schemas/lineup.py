from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.player import PlayerRead

# Scorecard position numbers -> letter codes. 10 is the extra hitter / DH slot.
POSITION_NUMBERS = {
    "1": "P",
    "2": "C",
    "3": "1B",
    "4": "2B",
    "5": "3B",
    "6": "SS",
    "7": "LF",
    "8": "CF",
    "9": "RF",
    "10": "DH",
}
POSITION_CODES = set(POSITION_NUMBERS.values()) | {"EH", "PH", "PR"}


class LineupEntryCreate(BaseModel):
    player_id: int
    batting_slot: int = Field(ge=1)
    position: str
    inning_entered: int | None = Field(default=None, ge=1)

    @field_validator("position")
    @classmethod
    def normalize_position(cls, value: str) -> str:
        code = POSITION_NUMBERS.get(value.strip(), value.strip().upper())
        if code not in POSITION_CODES:
            raise ValueError(
                f"Unknown position '{value}'. Use 1-10 or one of: {', '.join(sorted(POSITION_CODES))}"
            )
        return code


class LineupEntryRead(BaseModel):
    id: int
    game_id: int
    roster_id: int
    player_id: int
    batting_slot: int
    position: str
    inning_entered: int | None
    player: PlayerRead

    model_config = ConfigDict(from_attributes=True)
