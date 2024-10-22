from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum

class StudyEntityType(Enum):
    GROUP = "group"
    TEACHER = "teacher"

@dataclass
class Lesson:
    index: int
    start_time: datetime
    end_time: datetime
    subjects: list[str]
    cor_entities: list[str]
    # cor_entities meaning corresponding entities
    # if a lesson is provided for a group, a cor entity is a teacher (and vice versa)
    cabinets: list[str]

@dataclass
class Day:
    study_entity_kind: StudyEntityType
    study_entity_name: str
    date: date
    lessons: list[Lesson]
