from typing import Generic, Literal, TypeVar, Optional
from pydantic.generics import GenericModel

T = TypeVar('T')

class ApiResponse(GenericModel, Generic[T]):
    status: Literal["Success", "Error"]
    message: Optional[str] = None
    data: Optional[T] = None
    
    class Config:
        from_attributes = True