from typing import List
from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from shared import main_logger, LEXICON
from keyboards import help_kb, default_kb
from logic import process_lessons_tokens
from api import req_week
from logic import res_to_day, bells_logic
from database import engine, StudyEntity, find_teachers

user_router = Router()


@user_router.message(F.text.lower().startswith('пары'))
async def handle_lessons(msg: Message, tokens: List[str]):
    processed = process_lessons_tokens(tokens, msg.chat.id)
    # processed ['lessons', 'teacher' (kind), '1' (api_id), '21.09.24']

    kind = processed[1]
    id = processed[2]
    query_date = processed[3]
    res = req_week(kind, id, query_date)
    day = res_to_day(res, query_date)
    result = day.to_msg()
    await msg.answer(result)

@user_router.message(F.text.lower().startswith('помощь'))
async def handle_help(msg: Message, tokens: List[str]):
    match tokens[1]:
        case 'пары':
            result = LEXICON['help_lessons']
        case 'фио':
            result = LEXICON['help_fio']
        case 'звонки':
            result = LEXICON['help_bells']
        case _:
            result = LEXICON['help_generic']
    await msg.answer(result, reply_markup=help_kb)

@user_router.message(F.text.lower().startswith('звонки'))
async def handle_bells(msg: Message, tokens: List[str]):
    result = bells_logic(tokens[1])
    await msg.answer(result)

@user_router.message(F.text.lower().startswith("фио"))
async def handle_fio(msg: Message, tokens: List[str]):
    if not tokens[1]:
        result = LEXICON["exception"]
        
    with Session(engine) as session:
        teachers = find_teachers(tokens[1])

        if not teachers:
            result = LEXICON["reg_teacher_not_found"]
        elif len(teachers) == 1:
            result = f"""<b>👩‍🏫 Найден преподаватель:</b>

{teachers[0].name}

<i>Если вы не нашли нужного преподавателя, пишите в техподдержку.</i>"""
        else:
            result = "<b>👩‍🏫 Найдено несколько преподавателей:</b>\n\n"
            for i, teacher in enumerate(teachers):
                result += "\t" + str(i + 1) + ". " + teacher.name + "\n"

            result += "\n<i>Если вы не нашли нужного преподавателя, пишите в техподдержку.</i>"

    await msg.answer(result)

@user_router.message(F.text.lower().strip() == "клавиатура убрать")
async def handle_hide_kb(msg: Message):
    if msg.chat.type != "private":
        await msg.reply(LEXICON["not_available_in_groups"])
        return

    result = LEXICON["kb_hide"]
    kb = ReplyKeyboardRemove()
    await msg.reply(result, reply_markup=kb)

@user_router.message(F.text.lower().strip() == "клавиатура показать")
async def handle_show_kb(msg: Message):
    if msg.chat.type != "private":
        await msg.reply(LEXICON["not_available_in_groups"])
        return

    result = LEXICON["kb_show"]
    kb = default_kb
    await msg.reply(result, reply_markup=kb)
