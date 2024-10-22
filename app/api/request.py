from datetime import date, timedelta
import json
import requests
from models import Lesson, Day
from models import StudyEntityType
from utils import api_url, req_headers, main_logger

# TODO: разбить это все по модулям

## Returns a dictionary that api sends back
def req_week(type: StudyEntityType, id: int, query_date: date):
    match type:
        case StudyEntityType.GROUP:
            url = api_url + "group/lessons/"
        case StudyEntityType.TEACHER:
            url = api_url + "teacher/lessons/"
    monday = query_date - timedelta(days=query_date.weekday())
    payload = gen_payload(type, id, monday)
    response = json.loads(requests.post(url, headers=req_headers, json=payload).text)
    return response

# Converts a dictionary to a Day obj
def res_to_day(res, query_date: date):
    if "group" in res:
        name = res["group"]["name"]
        kind = StudyEntityType.GROUP
    elif "teacher" in res:
        name = res["teacher"]["fio"]
        kind = StudyEntityType.TEACHER
    else:
        main_logger.error("Something went wrong in lessons_for_today...")
        raise

    weekday = query_date.weekday() + 1
    lessons = [];
    for lesson in res["lessons"]:
        if (lesson["weekday"] == weekday):
            lessons.append(lesson)

    return Day(kind, name, query_date, lessons)

# Combines lessons that have the same index in a given Day obj
def combine_simul(day):
    #TODO: переписать. это старое решение, похоже на говнокод
    unfiltered = []
    for lesson in day.lessons:
        cab = [] if not lesson["cabinet"] else [lesson["cabinet"]["name"]]
        match day.study_entity_kind:
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
        unfiltered.append(tmp)
    unfiltered.sort(key=lambda x: x.index)

    res = []
    for i in range(len(unfiltered) - 1):
        if unfiltered[i].index == unfiltered[i + 1].index:
            res.append(Lesson(
                index=unfiltered[i].index,
                start_time=unfiltered[i].start_time,
                end_time=unfiltered[i].end_time,
                subjects=unfiltered[i].subjects + unfiltered[i + 1].subjects,
                cor_entities=unfiltered[i].cor_entities + unfiltered[i + 1].cor_entities,
                cabinets=unfiltered[i].cabinets + unfiltered[i + 1].cabinets,
            ))
        elif unfiltered[i].index == unfiltered[i - 1].index:
            continue
        else:
            res.append(unfiltered[i])
    res.append(unfiltered[len(unfiltered) - 1]) # FIXME: если уроков нет, то бросает ошибку. Должно выдавать просто пустой массив
    return Day(day.study_entity_kind, day.study_entity_name, day.date, res)

# Converts a Day obj to a human readable format
def day_to_msg(day):
    match day.study_entity_kind:
        case StudyEntityType.GROUP:
            cor_entity_str = "Преподаватель не указан"
        case StudyEntityType.TEACHER:
            cor_entity_str = "Группа не указана"
    result = f"""<b>{day.study_entity_name}</b>
{str(day.date.strftime("%A"))}, {len(day.lessons)} уроков
{str(day.date.strftime("%d.%m.%y"))}

"""
    if not day.lessons:
        result += """————| <b>Нет расписания</b> |————

<b>На этот день распиания пока нет...</b>"""
        return result

    for lesson in day.lessons:
        subject_string =  " | ".join(lesson.subjects) if (len(lesson.subjects) > 0) else "<i>Предмет не указан</i>"
        name_string = " | ".join(lesson.cor_entities) if (len(lesson.cor_entities) > 0) else f"<i>{cor_entity_str}</i>"
        cabinet_string = " | ".join(lesson.cabinets) if (len(lesson.cabinets) > 0) else "<i>Кабинет не указан</i>"

        result += "——————| <b>" + str(lesson.index) + " урок</b>" + " |——————\n\n"
        result += "⏳ " + lesson.start_time + " — " + lesson.end_time + "\n"
        result += "📖 <b>" + subject_string + "</b>\n"
        result += "🎓 " + name_string + "\n"
        result += "🔑 " + cabinet_string + "\n\n"
    return result

def gen_payload(type: StudyEntityType, id: int, query_date: date):
    res = dict()
    match type:
        case StudyEntityType.GROUP:
            res["groupId"] = id
        case StudyEntityType.TEACHER:
            res["teacherId"] = id

    res["date"] = str(query_date)
    res["publicationId"] = "45fc8ddd-35e2-4d8e-9da1-a081a8edc11d"
    return res
