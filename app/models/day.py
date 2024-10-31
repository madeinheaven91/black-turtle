from dataclasses import dataclass
from datetime import date
from typing import DefaultDict

from .models import Lesson, StudyEntityType
from app.shared import lessons_declension, LEXICON

@dataclass
class Day:
    study_entity_kind: StudyEntityType
    study_entity_name: str
    date: date
    lessons: list[Lesson]

    def __post_init__(self):
        self.lessons = sorted(self.lessons, key=lambda lesson: lesson.index)
        self.lessons = combine_simul(self)

    def to_msg(self):
        if not self.lessons:
            result = f"""<b>{self.study_entity_name}
{str(self.date.strftime("%A"))}
{str(self.date.strftime("%d.%m.%y"))}</b>

"""
            result += LEXICON["no_lessons"]
            return result

        match self.study_entity_kind:
            case StudyEntityType.GROUP:
                cor_entity_str = "Преподаватель не указан"
            case StudyEntityType.TEACHER:
                cor_entity_str = "Группа не указана"

        result = f"""<b>{self.study_entity_name}
{str(self.date.strftime("%A"))}, {len(self.lessons)} {lessons_declension(len(self.lessons))}
{str(self.date.strftime("%d.%m.%y"))}</b>

"""
        for lesson in self.lessons:
            subject_string =  " | ".join(lesson.subjects) if (len(lesson.subjects) > 0) else "<i>Предмет не указан</i>"
            name_string = " | ".join(lesson.cor_entities) if (len(lesson.cor_entities) > 0) else f"<i>{cor_entity_str}</i>"
            cabinet_string = " | ".join(lesson.cabinets) if (len(lesson.cabinets) > 0) else "<i>Кабинет не указан</i>"

            result += "——————| <b>" + str(lesson.index) + " урок</b>" + " |——————\n\n"
            result += "⏳ " + str(lesson.start_time) + " — " + str(lesson.end_time) + "\n"
            result += "📖 <b>" + subject_string + "</b>\n"
            result += "🎓 " + name_string + "\n"
            result += "🔑 " + cabinet_string + "\n\n"
        return result

# Combines lessons that have the same index in a given Day obj
def combine_simul(day) -> list[Lesson]:
    if not day.lessons:
        return day.lessons

    grouped = DefaultDict(list)

    for lesson in day.lessons:
        grouped[lesson.index].append(lesson)

    combined = []
    for index, lessons in grouped.items():
        if len(lessons) == 1:
            combined.append(lessons[0])
        else:
            subjects, cabinets, cor_entities = [], [], []
            for lesson in lessons:
                subjects.extend(lesson.subjects)
                cor_entities.extend(lesson.cor_entities)
                cabinets.extend(lesson.cabinets)
            combined.append(Lesson(
                index=index,
                start_time=lessons[0].start_time,
                end_time=lessons[0].end_time,
                subjects=subjects,
                cor_entities=cor_entities,
                cabinets=cabinets
            ))
    return combined
