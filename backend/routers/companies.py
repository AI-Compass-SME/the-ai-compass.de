from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Company
from schemas import company as schemas
from services.session_store import session_store

router = APIRouter()

@router.post("/", response_model=schemas.CompanyResponse)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    """
    Create a new company profile.
    """
    new_company = session_store.create_company(company)
    return new_company
