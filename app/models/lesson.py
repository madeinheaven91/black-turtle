from dataclasses import dataclass
from datetime import datetime

@dataclass
class Lesson:
    id: int
    start_time: datetime
    end_time: datetime
    names: list[str]
    teachers: list[str]
    cabinets: list[str]

    def to_message(self) -> str:
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}\n"

test_lesson = Lesson(
    id=1,
    start_time=datetime(2022, 1, 1, 9, 0),
    end_time=datetime(2022, 1, 1, 10, 0),
    names=["name1", "name2"],
    teachers=["teacher1", "teacher2"],
    cabinets=["cabinet1", "cabinet2"],
)
