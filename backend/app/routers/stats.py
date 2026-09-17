from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.batting_line import BattingLine
from app.models.player import Player
from app.models.roster import Roster
from app.schemas.stats import BattingStats

router = APIRouter(prefix="/players", tags=["stats"])


@router.get("/{player_id}/batting-stats", response_model=BattingStats)
def get_batting_stats(player_id: int, season_id: int | None = None, db: Session = Depends(get_db)):
    player = db.get(Player, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    query = db.query(
        func.count(BattingLine.id),
        func.sum(BattingLine.at_bats),
        func.sum(BattingLine.runs),
        func.sum(BattingLine.hits),
        func.sum(BattingLine.doubles),
        func.sum(BattingLine.triples),
        func.sum(BattingLine.home_runs),
        func.sum(BattingLine.rbi),
        func.sum(BattingLine.walks),
        func.sum(BattingLine.strikeouts),
        func.sum(BattingLine.stolen_bases),
    ).filter(BattingLine.player_id == player_id)

    # season_id isn't a column on BattingLine — it lives on Roster, so
    # scoping to one season means joining through roster_id first.
    if season_id is not None:
        query = query.join(Roster, BattingLine.roster_id == Roster.id).filter(Roster.season_id == season_id)

    (
        games_played,
        at_bats,
        runs,
        hits,
        doubles,
        triples,
        home_runs,
        rbi,
        walks,
        strikeouts,
        stolen_bases,
    ) = query.one()

    # SUM()/COUNT() over zero rows comes back as None, not 0.
    at_bats = at_bats or 0
    hits = hits or 0
    batting_average = round(hits / at_bats, 3) if at_bats > 0 else 0.0

    return BattingStats(
        games_played=games_played or 0,
        at_bats=at_bats,
        runs=runs or 0,
        hits=hits,
        doubles=doubles or 0,
        triples=triples or 0,
        home_runs=home_runs or 0,
        rbi=rbi or 0,
        walks=walks or 0,
        strikeouts=strikeouts or 0,
        stolen_bases=stolen_bases or 0,
        batting_average=batting_average,
    )
