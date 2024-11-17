from sqlalchemy.orm import Session
from models.types import Types

def get_types(db: Session):
    return db.query(Types).all()