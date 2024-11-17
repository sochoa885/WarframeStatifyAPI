from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.ApiResponse import ApiResponse
from schemas.items import Items
from crud.items import get_items

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

@router.get("/", response_model=ApiResponse[List[Items]], summary="Get all items", description="Request to get all items")
def get_all(db: Session = Depends(get_db)):
    return ApiResponse(status="Success", data=get_items(db))

