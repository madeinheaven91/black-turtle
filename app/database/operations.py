from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from .connect import engine
from .tables import StudyEntity

def find_teachers(queue: str):
    with Session(engine) as session:
        teachers = session.query(StudyEntity).filter(StudyEntity.kind == "teacher", StudyEntity.name.ilike(f"%{queue}%")).all()
        return teachers

def find_groups(queue: str):
    with Session(engine) as session:
        teachers = session.query(StudyEntity).filter(StudyEntity.kind == "group", StudyEntity.name.ilike(f"%{queue}%")).all()
        return teachers
