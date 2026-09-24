from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models.game import Game
from app.models.lineup_entry import LineupEntry
from app.models.roster_entry import RosterEntry
from app.schemas.game import GameCreate, GameRead, GameUpdate
from app.schemas.lineup import LineupEntryCreate, LineupEntryRead

router = APIRouter(prefix="/games", tags=["games"])


@router.post("/", response_model=GameRead, status_code=201)
def create_game(game_data: GameCreate, db: Session = Depends(get_db)):
    game = Game(**game_data.model_dump())
    db.add(game)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="A game's home and away rosters must be different")
    db.refresh(game)
    return game


@router.get("/", response_model=list[GameRead])
def list_games(db: Session = Depends(get_db)):
    return db.query(Game).all()


@router.get("/{game_id}", response_model=GameRead)
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.get(Game, game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


def _load_lineups(db: Session, game_id: int, roster_id: int | None = None):
    query = (
        db.query(LineupEntry)
        .options(selectinload(LineupEntry.player))
        .filter(LineupEntry.game_id == game_id)
    )
    if roster_id is not None:
        query = query.filter(LineupEntry.roster_id == roster_id)
    return query.order_by(
        LineupEntry.roster_id,
        LineupEntry.batting_slot,
        LineupEntry.inning_entered.asc().nulls_first(),
        LineupEntry.id,
    ).all()


@router.get("/{game_id}/lineups", response_model=list[LineupEntryRead])
def get_game_lineups(game_id: int, db: Session = Depends(get_db)):
    if db.get(Game, game_id) is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return _load_lineups(db, game_id)


@router.put("/{game_id}/lineups/{roster_id}", response_model=list[LineupEntryRead])
def replace_team_lineup(
    game_id: int,
    roster_id: int,
    entries: list[LineupEntryCreate],
    db: Session = Depends(get_db),
):
    game = db.get(Game, game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    if roster_id not in (game.home_roster_id, game.away_roster_id):
        raise HTTPException(status_code=400, detail="That roster isn't playing in this game")

    on_roster = {
        row.player_id
        for row in db.query(RosterEntry.player_id).filter(RosterEntry.roster_id == roster_id)
    }
    missing = {e.player_id for e in entries} - on_roster
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Players not on this roster: {sorted(missing)}",
        )

    db.query(LineupEntry).filter(
        LineupEntry.game_id == game_id, LineupEntry.roster_id == roster_id
    ).delete(synchronize_session=False)
    for e in entries:
        db.add(LineupEntry(game_id=game_id, roster_id=roster_id, **e.model_dump()))
    db.commit()
    return _load_lineups(db, game_id, roster_id)


@router.patch("/{game_id}", response_model=GameRead)
def update_game(game_id: int, game_data: GameUpdate, db: Session = Depends(get_db)):
    game = db.get(Game, game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    updates = game_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(game, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="A game's home and away rosters must be different")
    db.refresh(game)
    return game


@router.delete("/{game_id}", status_code=204)
def delete_game(game_id: int, db: Session = Depends(get_db)):
    game = db.get(Game, game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    db.delete(game)
    db.commit()
