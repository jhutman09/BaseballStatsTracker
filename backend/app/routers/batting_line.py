from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.batting_line import BattingLine
from app.schemas.batting_line import BattingLineCreate, BattingLineRead, BattingLineUpdate

router = APIRouter(prefix="/batting-lines", tags=["batting-lines"])


@router.post("/", response_model=BattingLineRead, status_code=201)
def create_batting_line(line_data: BattingLineCreate, db: Session = Depends(get_db)):
    line = BattingLine(**line_data.model_dump())
    db.add(line)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Player already has a batting line for this game")
    db.refresh(line)
    return line


@router.get("/", response_model=list[BattingLineRead])
def list_batting_lines(db: Session = Depends(get_db)):
    return db.query(BattingLine).all()


@router.get("/{batting_line_id}", response_model=BattingLineRead)
def get_batting_line(batting_line_id: int, db: Session = Depends(get_db)):
    line = db.get(BattingLine, batting_line_id)
    if line is None:
        raise HTTPException(status_code=404, detail="Batting line not found")
    return line


@router.patch("/{batting_line_id}", response_model=BattingLineRead)
def update_batting_line(batting_line_id: int, line_data: BattingLineUpdate, db: Session = Depends(get_db)):
    line = db.get(BattingLine, batting_line_id)
    if line is None:
        raise HTTPException(status_code=404, detail="Batting line not found")

    updates = line_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(line, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Player already has a batting line for this game")
    db.refresh(line)
    return line


@router.delete("/{batting_line_id}", status_code=204)
def delete_batting_line(batting_line_id: int, db: Session = Depends(get_db)):
    line = db.get(BattingLine, batting_line_id)
    if line is None:
        raise HTTPException(status_code=404, detail="Batting line not found")

    db.delete(line)
    db.commit()
