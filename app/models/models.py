from dataclasses import dataclass
from datetime import datetime
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

