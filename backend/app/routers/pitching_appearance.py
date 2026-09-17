from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.pitching_appearance import PitchingAppearance
from app.schemas.pitching_appearance import (
    PitchingAppearanceCreate,
    PitchingAppearanceRead,
    PitchingAppearanceUpdate,
)

router = APIRouter(prefix="/pitching-appearances", tags=["pitching-appearances"])


@router.post("/", response_model=PitchingAppearanceRead, status_code=201)
def create_pitching_appearance(appearance_data: PitchingAppearanceCreate, db: Session = Depends(get_db)):
    appearance = PitchingAppearance(**appearance_data.model_dump())
    db.add(appearance)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Player already has a pitching appearance for this game")
    db.refresh(appearance)
    return appearance


@router.get("/", response_model=list[PitchingAppearanceRead])
def list_pitching_appearances(db: Session = Depends(get_db)):
    return db.query(PitchingAppearance).all()


@router.get("/{appearance_id}", response_model=PitchingAppearanceRead)
def get_pitching_appearance(appearance_id: int, db: Session = Depends(get_db)):
    appearance = db.get(PitchingAppearance, appearance_id)
    if appearance is None:
        raise HTTPException(status_code=404, detail="Pitching appearance not found")
    return appearance


@router.patch("/{appearance_id}", response_model=PitchingAppearanceRead)
def update_pitching_appearance(
    appearance_id: int, appearance_data: PitchingAppearanceUpdate, db: Session = Depends(get_db)
):
    appearance = db.get(PitchingAppearance, appearance_id)
    if appearance is None:
        raise HTTPException(status_code=404, detail="Pitching appearance not found")

    updates = appearance_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(appearance, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Player already has a pitching appearance for this game")
    db.refresh(appearance)
    return appearance


@router.delete("/{appearance_id}", status_code=204)
def delete_pitching_appearance(appearance_id: int, db: Session = Depends(get_db)):
    appearance = db.get(PitchingAppearance, appearance_id)
    if appearance is None:
        raise HTTPException(status_code=404, detail="Pitching appearance not found")

    db.delete(appearance)
    db.commit()
