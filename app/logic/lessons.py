from datetime import date
from app.models import StudyEntityType, Day, Lesson
from app.shared import main_logger, LEXICON

# Converts a dictionary to a Day obj
def res_to_day(dic, query_date: date):
    if "group" in dic:
        name = dic["group"]["name"]
        kind = StudyEntityType.GROUP
    elif "teacher" in dic:
        name = dic["teacher"]["fio"]
        kind = StudyEntityType.TEACHER
    else:
        raise Exception("watafuk?")

    weekday = query_date.weekday() + 1
    lessons = [];
    for lesson in dic["lessons"]:
        if (lesson["weekday"] == weekday):
            cab = [] if not lesson["cabinet"] else [lesson["cabinet"]["name"]]
            match kind:
                case StudyEntityType.GROUP:
                    cor_entities = [lesson["teachers"][0]["fio"]] or []
                case StudyEntityType.TEACHER:
                    cor_entities = [lesson["unionGroups"][0]["group"]["name"]] or []
            tmp = Lesson(
                index=lesson["lesson"],
                start_time=lesson["startTime"],
                end_time=lesson["endTime"],
                subjects=[lesson["subject"]["name"]] or [],
                cor_entities=cor_entities,
                cabinets=cab,
            )
            lessons.append(tmp)

    return Day(kind, name, query_date, lessons)
