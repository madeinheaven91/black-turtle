from datetime import date, timedelta
import json
import requests
from app.models import StudyEntityType
from app.shared import api_url, req_headers, main_logger

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

def gen_payload(type: StudyEntityType, id: int, query_date: date):
    res = dict()
    match type:
        case StudyEntityType.GROUP:
            res["groupId"] = id
        case StudyEntityType.TEACHER:
            res["teacherId"] = id

    res["date"] = str(query_date)
    # res["publicationId"] = "45fc8ddd-35e2-4d8e-9da1-a081a8edc11d"
    res["publicationId"] = "4a1e0b67-8c36-4082-809d-97fe970928d4"
    return res
