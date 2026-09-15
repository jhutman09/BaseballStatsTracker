from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.season import Season
from app.schemas.season import SeasonCreate, SeasonRead, SeasonUpdate

router = APIRouter(prefix="/seasons", tags=["seasons"])


@router.post("/", response_model=SeasonRead, status_code=201)
def create_season(season_data: SeasonCreate, db: Session = Depends(get_db)):
    season = Season(**season_data.model_dump())
    db.add(season)
    db.commit()
    db.refresh(season)
    return season


@router.get("/", response_model=list[SeasonRead])
def list_seasons(db: Session = Depends(get_db)):
    return db.query(Season).all()


@router.get("/{season_id}", response_model=SeasonRead)
def get_season(season_id: int, db: Session = Depends(get_db)):
    season = db.get(Season, season_id)
    if season is None:
        raise HTTPException(status_code=404, detail="Season not found")
    return season


@router.patch("/{season_id}", response_model=SeasonRead)
def update_season(season_id: int, season_data: SeasonUpdate, db: Session = Depends(get_db)):
    season = db.get(Season, season_id)
    if season is None:
        raise HTTPException(status_code=404, detail="Season not found")

    updates = season_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(season, field, value)

    db.commit()
    db.refresh(season)
    return season


@router.delete("/{season_id}", status_code=204)
def delete_season(season_id: int, db: Session = Depends(get_db)):
    season = db.get(Season, season_id)
    if season is None:
        raise HTTPException(status_code=404, detail="Season not found")

    db.delete(season)
    db.commit()
