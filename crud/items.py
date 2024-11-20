from sqlalchemy.orm import Session
from models.items import Items, FortyEightHours, NinetyDays

def get_items(db: Session):
    return db.query(Items).all()

def get_mods(db: Session):
    return db.query(Items).filter(Items.type_id == 3).all()

def get_arcanes(db: Session):
    return db.query(Items).filter(Items.type_id == 2).all()

def get_item_by_name(db: Session, name: str):
    return db.query(Items).filter(Items.name_en == name).first()

def insert_item(db: Session, new_item: Items):
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item;

def insert_many_items(db: Session, items_data: list[dict]):
    db.bulk_insert_mappings(Items, items_data)
    db.commit()
    return True
    
def get_rank_0_forty_eight_hours_by_item_id(db: Session, item_id: int):
    return db.query(FortyEightHours).filter(FortyEightHours.item_id == item_id).filter(FortyEightHours.rank == 0).first()
    
def get_rank_max_forty_eight_hours_by_item_id(db: Session, item_id: int):
    return db.query(FortyEightHours).filter(FortyEightHours.item_id == item_id).filter(FortyEightHours.rank > 0).first()
    
def get_rank_0_ninety_days_by_item_id(db: Session, item_id: int):
    return db.query(NinetyDays).filter(NinetyDays.item_id == item_id).filter(NinetyDays.rank == 0).first()
    
def get_rank_max_ninety_days_by_item_id(db: Session, item_id: int):
    return db.query(NinetyDays).filter(NinetyDays.item_id == item_id).filter(NinetyDays.rank > 0).first()

def insert_forty_eight_hours(db: Session, forty_eight_hours_data: FortyEightHours):
    db.add(forty_eight_hours_data)
    db.commit()
    db.refresh(forty_eight_hours_data)
    return forty_eight_hours_data;

def insert_ninety_days(db: Session, ninety_days_data: NinetyDays):
    db.add(ninety_days_data)
    db.commit()
    db.refresh(ninety_days_data)
    return ninety_days_data;

def insert_many_forty_eight_hours(db: Session, data: list[dict]):
    db.bulk_insert_mappings(FortyEightHours, data)
    db.commit()
    return True

def insert_many_ninety_days(db: Session, data: list[dict]):
    db.bulk_insert_mappings(NinetyDays, data)
    db.commit()
    return True

def update_many_forty_eight_hours(db: Session, data: list[dict]):
    db.bulk_update_mappings(FortyEightHours, data)
    db.commit()
    return True

def update_many_ninety_days(db: Session, data: list[dict]):
    db.bulk_update_mappings(NinetyDays, data)
    db.commit()
    return True