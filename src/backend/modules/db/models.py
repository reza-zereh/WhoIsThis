from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Member(Base):
    __tablename__ = 'members'
    # columns
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    # relationships
    photos = relationship("Photo", back_populates="member")


class Model(Base):
    __tablename__ = 'models'
    # columns
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    # relationships
    photos = relationship("Embedding", back_populates="model")


class Photo(Base):
    __tablename__ = 'photos'
    # columns
    id = Column(Integer, primary_key=True, nullable=False)
    filename = Column(String)
    member_id = Column(Integer, ForeignKey("members.id"))
    is_main_photo = Column(Boolean, default=False)
    # relationships
    member = relationship("Member", back_populates="photos")


class Embedding(Base):
    __tablename__ = 'embeddings'
    # columns
    id = Column(Integer, primary_key=True, nullable=False)
    photo_id = Column(Integer, ForeignKey("photos.id"))
    model_id = Column(Integer, ForeignKey("models.id"))
    encoding = Column(String)
    # relationships
    model = relationship("Model", back_populates="embeddings")