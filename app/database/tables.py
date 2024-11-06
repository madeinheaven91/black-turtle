from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, BigInteger
from .connect import engine

class Base(DeclarativeBase):
    pass

class StudyEntity(Base):
    __tablename__ = "StudyEntity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    api_id: Mapped[int] = mapped_column(Integer)
    kind: Mapped[str] = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(64))

    chat: Mapped[Optional["Chat"]] = relationship("Chat", back_populates="study_entity")

class Chat(Base):
    __tablename__ = "Chat"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    kind: Mapped[str] = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(64))
    username: Mapped[Optional[str]] = mapped_column(String(64))
    study_entity_id: Mapped[Optional[int]] = mapped_column(ForeignKey("StudyEntity.id"))
    is_banned: Mapped[bool] = mapped_column(default=False)

    study_entity: Mapped["StudyEntity"] = relationship("StudyEntity",back_populates="chat")
    admin: Mapped[Optional["Admin"]] = relationship("Admin", back_populates="chat")

class Admin(Base):
    __tablename__ = "Admin"

    id: Mapped[int] = mapped_column(BigInteger, ForeignKey("Chat.id"), primary_key=True)
    level: Mapped[int] = mapped_column(Integer)

    chat: Mapped["Chat"] = relationship("Chat", back_populates="admin")

Base.metadata.create_all(engine)
