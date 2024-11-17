from sqlalchemy.orm import Session
from models.tags import Tags

def get_tags(db: Session):
    return db.query(Tags).all()