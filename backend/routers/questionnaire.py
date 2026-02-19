from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Question, Answer
from schemas import questionnaire as schemas

router = APIRouter()

@router.get("/", response_model=schemas.Questionnaire)
def get_questionnaire(db: Session = Depends(get_db)):
    """
    Fetch the full questionnaire with all questions and answers.
    """
    questions = db.query(Question).filter(Question.optional == False).all()
    # Note: We might want to include optional header questions too depending on UI logic
    # For v1 simple wizard, getting all non-optional questions is a good start.
    # Actually, let's just get ALL questions and let frontend filter if needed.
    questions = db.query(Question).order_by(Question.question_id).all()
    
    return {"questions": questions}
