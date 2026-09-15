from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.club import Club
from app.schemas.club import ClubCreate, ClubRead, ClubUpdate

router = APIRouter(prefix="/clubs", tags=["clubs"])


@router.post("/", response_model=ClubRead, status_code=201)
def create_club(club_data: ClubCreate, db: Session = Depends(get_db)):
    club = Club(**club_data.model_dump())
    db.add(club)
    db.commit()
    db.refresh(club)
    return club


@router.get("/", response_model=list[ClubRead])
def list_clubs(db: Session = Depends(get_db)):
    return db.query(Club).all()


@router.get("/{club_id}", response_model=ClubRead)
def get_club(club_id: int, db: Session = Depends(get_db)):
    club = db.get(Club, club_id)
    if club is None:
        raise HTTPException(status_code=404, detail="Club not found")
    return club


@router.patch("/{club_id}", response_model=ClubRead)
def update_club(club_id: int, club_data: ClubUpdate, db: Session = Depends(get_db)):
    club = db.get(Club, club_id)
    if club is None:
        raise HTTPException(status_code=404, detail="Club not found")

    updates = club_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(club, field, value)

    db.commit()
    db.refresh(club)
    return club


@router.delete("/{club_id}", status_code=204)
def delete_club(club_id: int, db: Session = Depends(get_db)):
    club = db.get(Club, club_id)
    if club is None:
        raise HTTPException(status_code=404, detail="Club not found")

    db.delete(club)
    db.commit()
