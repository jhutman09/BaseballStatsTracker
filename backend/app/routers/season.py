from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.season import Season
from app.schemas.season import SeasonCreate, SeasonRead

router = APIRouter(prefix="/seasons", tags=["seasons"])


@router.post("/", response_model=SeasonRead, status_code=201)
def create_season(season_data: SeasonCreate, db: Session = Depends(get_db)):
    # TODO:
    #   1. Build a Season ORM instance from season_data (it's already a
    #      validated Pydantic model at this point — see season_data.model_dump()
    #      for turning it into a dict of column values).
    #   2. Add it to the session (db.add(...)), commit, then db.refresh(...)
    #      so the auto-generated id comes back from the database.
    #   3. Return the Season object — FastAPI converts it to SeasonRead JSON
    #      automatically via response_model.
    pass


@router.get("/", response_model=list[SeasonRead])
def list_seasons(db: Session = Depends(get_db)):
    # TODO: query every Season row and return the list.
    pass


@router.get("/{season_id}", response_model=SeasonRead)
def get_season(season_id: int, db: Session = Depends(get_db)):
    # TODO:
    #   1. Look up one Season by its primary key (db.get(Season, season_id)).
    #   2. If nothing comes back, raise HTTPException(status_code=404,
    #      detail="Season not found") — FastAPI turns that into a proper
    #      404 response.
    #   3. Otherwise return the Season object.
    pass
