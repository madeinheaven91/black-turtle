from dataclasses import dataclass
from datetime import datetime
from enum import Enum

@dataclass
class Lesson:
    index: int
    start_time: datetime
    end_time: datetime
    subjects: list[str]
    teachers: list[str]
    cabinets: list[str]

test_lesson = Lesson(
    index=1,
    start_time=datetime(2022, 1, 1, 9, 0),
    end_time=datetime(2022, 1, 1, 10, 0),
    subjects=["name1", "name2"],
    teachers=["teacher1", "teacher2"],
    cabinets=["cabinet1", "cabinet2"],
)

class StudyEntityType(Enum):
    GROUP = "group"
    TEACHER = "teacher"
