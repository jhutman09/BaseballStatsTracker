from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamRead, TeamUpdate

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("/", response_model=TeamRead, status_code=201)
def create_team(team_data: TeamCreate, db: Session = Depends(get_db)):
    team = Team(**team_data.model_dump())
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


@router.get("/", response_model=list[TeamRead])
def list_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()


@router.get("/{team_id}", response_model=TeamRead)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.get(Team, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.patch("/{team_id}", response_model=TeamRead)
def update_team(team_id: int, team_data: TeamUpdate, db: Session = Depends(get_db)):
    team = db.get(Team, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    updates = team_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(team, field, value)

    db.commit()
    db.refresh(team)
    return team


@router.delete("/{team_id}", status_code=204)
def delete_team(team_id: int, db: Session = Depends(get_db)):
    team = db.get(Team, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    db.delete(team)
    db.commit()
