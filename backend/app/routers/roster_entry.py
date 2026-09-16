from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.roster_entry import RosterEntry
from app.schemas.roster_entry import RosterEntryCreate, RosterEntryRead, RosterEntryUpdate

router = APIRouter(prefix="/roster-entries", tags=["roster-entries"])


@router.post("/", response_model=RosterEntryRead, status_code=201)
def create_roster_entry(entry_data: RosterEntryCreate, db: Session = Depends(get_db)):
    entry = RosterEntry(**entry_data.model_dump())
    db.add(entry)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Player is already on this roster")
    db.refresh(entry)
    return entry


@router.get("/", response_model=list[RosterEntryRead])
def list_roster_entries(db: Session = Depends(get_db)):
    return db.query(RosterEntry).all()


@router.get("/{entry_id}", response_model=RosterEntryRead)
def get_roster_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.get(RosterEntry, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Roster entry not found")
    return entry


@router.patch("/{entry_id}", response_model=RosterEntryRead)
def update_roster_entry(entry_id: int, entry_data: RosterEntryUpdate, db: Session = Depends(get_db)):
    entry = db.get(RosterEntry, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Roster entry not found")

    updates = entry_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(entry, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Player is already on this roster")
    db.refresh(entry)
    return entry


@router.delete("/{entry_id}", status_code=204)
def delete_roster_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = db.get(RosterEntry, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Roster entry not found")

    db.delete(entry)
    db.commit()
