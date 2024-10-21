from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, PrimaryKeyConstraint
from .connect import engine

class Base(DeclarativeBase):
    pass

class StudyEntity(Base):
    __tablename__ = "study_entities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    api_id: Mapped[int] = mapped_column(Integer)
    kind: Mapped[str] = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(64))

    chat: Mapped[Optional["Chat"]] = relationship("Chat", back_populates="study_entity")

class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    kind: Mapped[str] = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(64))
    username: Mapped[Optional[str]] = mapped_column(String(64))
    study_entity_id: Mapped[Optional[int]] = mapped_column(ForeignKey("study_entities.id"))
    is_banned: Mapped[bool] = mapped_column(default=False)

    study_entity: Mapped["StudyEntity"] = relationship(back_populates="chat")



Base.metadata.create_all(engine)
