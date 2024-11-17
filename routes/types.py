from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.ApiResponse import ApiResponse
from schemas.types import Types
from crud.types import get_types

router = APIRouter(
    prefix="/types",
    tags=["types"],
)

@router.get("/", response_model=ApiResponse[List[Types]], summary="Get all types", description="Request to get all types")
def get_all(db: Session = Depends(get_db)):
    return ApiResponse(status="Success", data=get_types(db))