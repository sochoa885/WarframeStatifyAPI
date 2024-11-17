from pydantic import BaseModel, Field

class TagsBase(BaseModel):
    name: str = Field(..., description="Tag name")

class Tags(TagsBase):
    id: int

    class Config:
        from_attributes = True
        
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "warframe"
            }
        }