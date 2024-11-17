from pydantic import BaseModel, Field
from .tags import Tags
from .types import Types
from typing import List

class ItemsBase(BaseModel):
    name_en: str = Field(..., description="English item name")
    name_es: str = Field(..., description="Spanish item name")
    url_name: str = Field(..., description="Url")
    icon: str = Field(..., description="icon")
    
class DataBase(BaseModel):
    volume: int = Field(...)
    avg_price: float = Field(...)
    rank: int = Field(...)
    
class Data(DataBase):
    id: int
    
    class Config:
        from_attributes = True

class Items(ItemsBase):
    id: int
    tag: Tags
    type: Types
    forty_eight_hours: List[Data]
    ninety_days: List[Data]

    class Config:
        from_attributes = True