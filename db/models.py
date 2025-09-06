from sqlalchemy import (Column, Integer, String, Text, Boolean, DateTime, ForeignKey, SmallInteger, func,
                        UniqueConstraint
                        )
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=True)
    tg_id = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    codes = relationship("Code", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="user", cascade="all, delete-orphan")


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, unique=False, nullable=True)
    address = Column(Text, unique=True, nullable=False)
    city = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    codes = relationship("Code", back_populates="place", cascade="all, delete-orphan")


class Code(Base):
    __tablename__ = "codes"

    id = Column(Integer, primary_key=True, index=True)
    place_id = Column(Integer, ForeignKey("places.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    code = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    place = relationship("Place", back_populates="codes")
    user = relationship("User", back_populates="codes")
    comments = relationship("Comment", back_populates="code", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="code", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    code_id = Column(Integer, ForeignKey("codes.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    code = relationship("Code", back_populates="comments")
    user = relationship("User", back_populates="comments")


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    code_id = Column(Integer, ForeignKey("codes.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vote_type = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    code = relationship("Code", back_populates="votes")
    user = relationship("User", back_populates="votes")


