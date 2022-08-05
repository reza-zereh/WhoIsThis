from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Member(Base):
    __tablename__ = 'members'
    # columns
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    # relationships
    photos = relationship("Photo", back_populates="member")


class Photo(Base):
    __tablename__ = 'photos'
    # columns
    id = Column(Integer, primary_key=True, nullable=False)
    filename = Column(String)
    embedding = Column(String)
    member_id = Column(Integer, ForeignKey("members.id"))
    # relationships
    member = relationship("Member", back_populates="photos")