from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.game import Game
from app.schemas.game import GameCreate, GameRead, GameUpdate

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
