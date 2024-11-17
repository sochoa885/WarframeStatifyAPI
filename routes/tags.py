from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.ApiResponse import ApiResponse
from schemas.tags import Tags
from crud.tags import get_tags

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
)

@router.get("/", response_model=ApiResponse[List[Tags]], summary="Get all tags", description="Request to get all tags")
def get_all(db: Session = Depends(get_db)):
    return ApiResponse(status="Success", data=get_tags(db))