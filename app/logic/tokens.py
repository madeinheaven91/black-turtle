from datetime import datetime, date, timedelta
from typing import Any
from app.exceptions import StudyEntityNotFoundError, StudyEntityNotSelectedError, WrongStudyEntityKindError
from app.models import StudyEntityType
from app.shared import relative_day_tokens, absolute_day_tokens, day_tokens, week_tokens, main_logger
from app.database import engine, StudyEntity, Chat
from sqlalchemy.orm import Session

def is_day_token(string):
    if string in relative_day_tokens or string in absolute_day_tokens:
        return True
    else:
        try:
            datetime.strptime(string, '%d.%m.%Y')
            return True
        except:
            return False

def is_week_token(string):
    if string in week_tokens:
        return True
    else:
        return False

def extract_lessons_tokens(tokens: list[str]):
    tokens = tokens[1:]
    day_token_index, week_token_index = None, None
    day_token, week_token = "", ""

    for i, token in enumerate(tokens):
        if not day_token and is_day_token(token):
                day_token_index, day_token = i, token
        if not week_token and is_week_token(token):
                week_token_index, week_token = i, token

    if day_token_index == 0 or week_token_index == 0:
        return ["пары", "", day_token, week_token]

    if day_token_index:
        name_token = " ".join(tokens[:day_token_index]).strip()
    else:
        if week_token_index:
            name_token = " ".join(tokens[:week_token_index]).strip()
        else:
            name_token = " ".join(tokens).strip()

    return ["пары", name_token, day_token, week_token]


# [пары, 921, пн, след]
# --->
# [ 'lessons', kind, api_id, query_date ]
def process_lessons_tokens(tokens: list[str], chat_id: int) -> list[Any]:

    study_entity_name = tokens[1]
    day_token = tokens[2]
    week_token = tokens[3]

    with Session(engine) as session:
        if not study_entity_name:
            chat = session.query(Chat).filter(Chat.id == chat_id).first()
            if not chat:
                raise StudyEntityNotSelectedError(f"Study entity not selected in chat {chat_id}")
            study_entity = session.query(StudyEntity).filter(StudyEntity.id == chat.study_entity_id).first()
        else:
            study_entity = session.query(StudyEntity).filter(StudyEntity.name.ilike(f"%{study_entity_name}%")).first()
        if study_entity:
            match study_entity.kind:
                case "teacher":
                    kind = StudyEntityType.TEACHER
                case "group":
                    kind = StudyEntityType.GROUP
                case _:
                    raise WrongStudyEntityKindError(f"Wrong study entity kind: {study_entity.kind}. Only 'teacher' or 'group' is allowed")
            api_id = study_entity.api_id

            if day_token not in day_tokens:
                query_date = datetime.strptime(day_token, '%d.%m.%Y').date() if day_token else date.today()
            else:
                if day_token in absolute_day_tokens:
                    match day_token:
                        case "понедельник" | "пн" | "пон":
                            query_date = date.today() - timedelta(days=date.today().weekday())
                        case "вторник" | "вт" | "втор":
                            query_date = date.today() - timedelta(days=date.today().weekday() - 1)
                        case "среда" | "ср" | "сред":
                            query_date = date.today() - timedelta(days=date.today().weekday() - 2)
                        case "четверг" | "чт" | "чет":
                            query_date = date.today() - timedelta(days=date.today().weekday() - 3)
                        case "пятница" | "пт" | "пят":
                            query_date = date.today() - timedelta(days=date.today().weekday() - 4)
                        case "суббота" | "сб" | "суб":
                            query_date = date.today() - timedelta(days=date.today().weekday() - 5)
                        case "воскресенье" | "вс" | "вос" | "воск":
                            query_date = date.today() - timedelta(days=date.today().weekday() - 6)
                    match week_token:
                        # case "эта" | "этот" | "текущая" | "":
                        case "след" | "следующая" | "следующий" | "следующее":
                            query_date = query_date + timedelta(7)
                        case "прош" | "прошлая" | "прошлый" | "прошлое":
                            query_date = query_date - timedelta(7)

                else:
                    match day_token:
                        case "" | "сегодня":
                            query_date = date.today()
                        case "завтра":
                            query_date = date.today() + timedelta(days=1)
                        case "вчера":
                            query_date = date.today() - timedelta(days=1)

                
            processed = ["lessons", kind, api_id, query_date]
            return processed
        else:
            raise StudyEntityNotFoundError(f"Study entity not found (name: {study_entity_name})")
