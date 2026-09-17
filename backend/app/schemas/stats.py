from pydantic import BaseModel


class BattingStats(BaseModel):
    games_played: int
    at_bats: int
    runs: int
    hits: int
    doubles: int
    triples: int
    home_runs: int
    rbi: int
    walks: int
    strikeouts: int
    stolen_bases: int
    batting_average: float
