from fastapi import APIRouter
from .questionnaire import router as questionnaire_router
from .companies import router as companies_router
from .responses import router as responses_router
from .results import router as results_router

api_router = APIRouter()

api_router.include_router(questionnaire_router, prefix="/questionnaire", tags=["Questionnaire"])
api_router.include_router(companies_router, prefix="/companies", tags=["Companies"])
api_router.include_router(responses_router, prefix="/responses", tags=["Responses"])
api_router.include_router(results_router, prefix="/responses", tags=["Results"])
