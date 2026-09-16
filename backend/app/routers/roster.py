from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.roster import Roster
from app.schemas.roster import RosterCreate, RosterRead, RosterUpdate

router = APIRouter(prefix="/rosters", tags=["rosters"])


@router.post("/", response_model=RosterRead, status_code=201)
def create_roster(roster_data: RosterCreate, db: Session = Depends(get_db)):
    roster = Roster(**roster_data.model_dump())
    db.add(roster)
    db.commit()
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


@router.patch("/{roster_id}", response_model=RosterRead)
def update_roster(roster_id: int, roster_data: RosterUpdate, db: Session = Depends(get_db)):
    roster = db.get(Roster, roster_id)
    if roster is None:
        raise HTTPException(status_code=404, detail="Roster not found")

    updates = roster_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(roster, field, value)

    db.commit()
    db.refresh(roster)
    return roster


@router.delete("/{roster_id}", status_code=204)
def delete_roster(roster_id: int, db: Session = Depends(get_db)):
    roster = db.get(Roster, roster_id)
    if roster is None:
        raise HTTPException(status_code=404, detail="Roster not found")

    db.delete(roster)
    db.commit()
