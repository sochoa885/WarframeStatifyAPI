from sqlalchemy import Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship
from database.database import Base

class Items(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name_en = Column(String, index=True)
    name_es = Column(String, nullable=False)
    url_name = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("types.id"), nullable=False)
    tag = relationship("Tags", back_populates="items")
    type = relationship("Types", back_populates="items")
    forty_eight_hours = relationship("FortyEightHours", back_populates="item", cascade="all, delete-orphan")
    ninety_days = relationship("NinetyDays", back_populates="item", cascade="all, delete-orphan")

class FortyEightHours(Base):
    __tablename__ = "forty_eight_hours"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    volume = Column(Integer, nullable=False)
    avg_price = Column(Numeric, nullable=False)
    rank = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey("items.id", ondelete='CASCADE'), nullable=False)
    item = relationship("Items", back_populates="forty_eight_hours")


class NinetyDays(Base):
    __tablename__ = "ninety_days"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    volume = Column(Integer, nullable=False)
    avg_price = Column(Numeric, nullable=False)
    rank = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey("items.id", ondelete='CASCADE'), nullable=False)
    item = relationship("Items", back_populates="ninety_days")