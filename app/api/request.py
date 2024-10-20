from datetime import date, timedelta
import json
import requests
from models import Lesson
from models import StudyEntityType
from utils import api_url, req_headers

### Returns a dictionary that api sends back
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

def lessons_for_today(res, query_date: date):
    weekday = query_date.weekday() + 1
    result = [];
    for lesson in res["lessons"]:
        if (lesson["weekday"] == weekday):
            result.append(lesson)
    return result

def dictionary_to_lessons(dic):
    #TODO: переписать. это старое решение, похоже на говнокод
    unfiltered = []
    for lesson in dic:
        if lesson["cabinet"] is None:
            cab = []
        else: 
            cab = [lesson["cabinet"]["name"]]
        tmp = Lesson(
            index=lesson["lesson"],
            start_time=lesson["startTime"],
            end_time=lesson["endTime"],
            subjects=[lesson["subject"]["name"]] or [],
            teachers=[lesson["teachers"][0]["fio"]] or [],
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
                teachers=unfiltered[i].teachers + unfiltered[i + 1].teachers,
                cabinets=unfiltered[i].cabinets + unfiltered[i + 1].cabinets,
            ))
        elif unfiltered[i].index == unfiltered[i - 1].index:
            continue
        else:
            res.append(unfiltered[i])
    res.append(unfiltered[len(unfiltered) - 1])
    return res

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
