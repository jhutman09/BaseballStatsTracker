from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.player import Player
from app.schemas.player import PlayerCreate, PlayerRead, PlayerUpdate

router = APIRouter(prefix="/players", tags=["players"])


@router.post("/", response_model=PlayerRead, status_code=201)
def create_player(player_data: PlayerCreate, db: Session = Depends(get_db)):
    player = Player(**player_data.model_dump())
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


@router.post("/bulk", response_model=list[PlayerRead], status_code=201)
def create_players_bulk(players_data: list[PlayerCreate], db: Session = Depends(get_db)):
    players = [Player(**p.model_dump()) for p in players_data]
    db.add_all(players)
    db.commit()
    for player in players:
        db.refresh(player)
    return players


@router.get("/", response_model=list[PlayerRead])
def list_players(db: Session = Depends(get_db)):
    return db.query(Player).all()


@router.get("/{player_id}", response_model=PlayerRead)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.get(Player, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@router.patch("/{player_id}", response_model=PlayerRead)
def update_player(player_id: int, player_data: PlayerUpdate, db: Session = Depends(get_db)):
    player = db.get(Player, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    updates = player_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(player, field, value)

    db.commit()
    db.refresh(player)
    return player


@router.delete("/{player_id}", status_code=204)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = db.get(Player, player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    db.delete(player)
    db.commit()
