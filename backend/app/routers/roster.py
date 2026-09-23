from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.models.player import Player
from app.models.roster import Roster
from app.models.roster_entry import RosterEntry
from app.schemas.roster import RosterCreate, RosterRead, RosterUpdate
from app.schemas.roster_entry import RosterEntryWithPlayer, RosterPlayerCreate

router = APIRouter(prefix="/rosters", tags=["rosters"])


@router.post("/", response_model=RosterRead, status_code=201)
def create_roster(roster_data: RosterCreate, db: Session = Depends(get_db)):
    roster = Roster(**roster_data.model_dump())
    db.add(roster)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A roster with this name, or for this club and season, already exists",
        )
    db.refresh(roster)
    return roster


@router.get("/", response_model=list[RosterRead])
def list_rosters(db: Session = Depends(get_db)):
    return db.query(Roster).all()


@router.get("/{roster_id}", response_model=RosterRead)
def get_roster(roster_id: int, db: Session = Depends(get_db)):
    roster = db.get(Roster, roster_id)
    if roster is None:
        raise HTTPException(status_code=404, detail="Roster not found")
    return roster


@router.get("/{roster_id}/entries", response_model=list[RosterEntryWithPlayer])
def list_roster_entries(roster_id: int, db: Session = Depends(get_db)):
    if db.get(Roster, roster_id) is None:
        raise HTTPException(status_code=404, detail="Roster not found")
    return (
        db.query(RosterEntry)
        .options(selectinload(RosterEntry.player))
        .filter(RosterEntry.roster_id == roster_id)
        .all()
    )


@router.post(
    "/{roster_id}/players/bulk",
    response_model=list[RosterEntryWithPlayer],
    status_code=201,
)
def add_players_to_roster(
    roster_id: int, players_data: list[RosterPlayerCreate], db: Session = Depends(get_db)
):
    if db.get(Roster, roster_id) is None:
        raise HTTPException(status_code=404, detail="Roster not found")

    entries = []
    for data in players_data:
        player = Player(first_name=data.first_name, last_name=data.last_name)
        entry = RosterEntry(player=player, roster_id=roster_id, jersey_number=data.jersey_number)
        db.add(entry)
        entries.append(entry)
    db.commit()
    for entry in entries:
        db.refresh(entry)
    return entries


@router.patch("/{roster_id}", response_model=RosterRead)
def update_roster(roster_id: int, roster_data: RosterUpdate, db: Session = Depends(get_db)):
    roster = db.get(Roster, roster_id)
    if roster is None:
        raise HTTPException(status_code=404, detail="Roster not found")

    updates = roster_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(roster, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A roster with this name, or for this club and season, already exists",
        )
    db.refresh(roster)
    return roster


@router.delete("/{roster_id}", status_code=204)
def delete_roster(roster_id: int, db: Session = Depends(get_db)):
    roster = db.get(Roster, roster_id)
    if roster is None:
        raise HTTPException(status_code=404, detail="Roster not found")

    db.delete(roster)
    db.commit()
