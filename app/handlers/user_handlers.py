from typing import List
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from sqlalchemy.orm import Session
from sqlalchemy import select, insert

from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, KeyboardButton, Message,
                           ReplyKeyboardMarkup, ReplyKeyboardRemove)
from aiogram.utils.keyboard import (InlineKeyboardBuilder, KeyboardBuilder,
                                    ReplyKeyboardBuilder)

from fsm import Registration
from utils import main_logger
from database import Chat
from lexicon import LEXICON
from keyboards import help_kb, greeting_kb, reg_group_or_teacher_kb, reg_cancel_kb, default_kb
from logic import process_lessons_tokens
from database import engine, StudyEntity, Chat

router = Router()



### START AND REGISTRATION
# TODO: вынести логику старта и регистрации в отедльный файл

@router.message(Command("start"))
async def cmd_start(msg: Message) -> None:
    with Session(engine) as session:
        res = session.execute(select(Chat).where(Chat.id == msg.chat.id))
        existing_chat = res.first()

        if not existing_chat:
            main_logger.info(f"New chat! ID: {msg.chat.id}, type: {msg.chat.type}")
            match msg.chat.type:
                case "private":
                    session.add(Chat(id=msg.chat.id, kind="private", name=msg.from_user.full_name, username=msg.from_user.username))
                    session.commit()
                case _:
                    session.execute(Chat(id=msg.chat.id, kind="group", name=msg.chat.title))
                    session.commit()
        else:
            main_logger.info(f"Chat already exists! ID: {msg.chat.id}, type: {msg.chat.type}")

    try:
        await msg.answer(LEXICON['/start'], reply_markup=greeting_kb)
    except Exception as e:
        main_logger.error(e)


@router.callback_query(F.data == "reg_yes")
async def reg_yes(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        LEXICON['reg_group_or_teacher'],
        reply_markup=reg_group_or_teacher_kb,
    )
    await callback.answer()


@router.callback_query(F.data == "reg_group")
async def reg_choose_group_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(
        LEXICON["reg_enter_group"],
        reply_markup=reg_cancel_kb,
    )
    await state.set_state(Registration.select_group)
    await callback.answer()


@router.callback_query(F.data == "reg_teacher")
async def reg_choose_teacher_callback( callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text(
        LEXICON["reg_enter_teacher"],
        reply_markup=reg_cancel_kb,
    )
    await state.set_state(Registration.select_teacher)
    await callback.answer()


@router.callback_query(F.data == "reg_no")
async def reg_no(callback: CallbackQuery) -> None:
    await callback.message.edit_text(LEXICON["reg_cancel"])
    await callback.answer()


@router.message(Registration.select_group)
async def select_group(message: Message, state: FSMContext) -> None:
    with Session(engine) as session:
        group = session.query(StudyEntity).filter(StudyEntity.name == message.text, StudyEntity.kind == "group").first()
        if not group:
            await state.set_state(Registration.select_group)
            await message.answer(LEXICON["reg_group_not_found"], reply_markup=reg_cancel_kb,)
            main_logger.error("Unknown group (" + message.text + ")")
            return
        else:
            chat = session.query(Chat).filter(Chat.id == message.chat.id).first()
            chat.study_entity_id = group.id
            session.commit()
            await message.answer(LEXICON["reg_group_selected"], reply_markup=default_kb)
            await state.clear()


@router.message(Registration.select_teacher)
async def select_teacher(message: Message, state: FSMContext) -> None:
    with Session(engine) as session:
        teachers = session.query(StudyEntity).filter(StudyEntity.name.ilike(f"%{message.text}%"), StudyEntity.kind == "teacher").all()
        if not teachers:
            await state.set_state(Registration.select_teacher)
            await message.answer(LEXICON["reg_teacher_not_found"], reply_markup=reg_cancel_kb,)
            main_logger.error("Unknown teacher (" + message.text + ")")
            return
        else:
            if len(teachers) == 1:
                teacher = teachers[0]
                chat = session.query(Chat).filter(Chat.id == message.chat.id).first()
                chat.study_entity_id = teacher.id
                session.commit()
                await message.answer(LEXICON["reg_teacher_selected"], reply_markup=default_kb)
                await state.clear()
            else:
                msg = "Найдено несколько преподавателей...\n\n"

                kb_builder = InlineKeyboardBuilder()

                for i, teacher in enumerate(teachers):
                    msg += str(i + 1) + ". " + teacher.name + "\n"
                    kb_builder.add(InlineKeyboardButton(text=str(i + 1), callback_data=f"select_teacher_{teacher.id}"))
                kb = kb_builder.as_markup(resize_keyboard=True)

                msg += "\nВыберите номер преподавателя из списка ниже."
                await message.answer(msg, reply_markup=kb)
                return


@router.callback_query(F.data.startswith("select_teacher_"))
async def select_teacher_callback(callback: CallbackQuery, state: FSMContext) -> None:
    with Session(engine) as session:
        teacher = session.query(StudyEntity).filter(StudyEntity.id == int(callback.data.split("_")[2])).first()
        chat = session.query(Chat).filter(Chat.id == callback.message.chat.id).first()
        chat.study_entity_id = teacher.id
        session.commit()
        await callback.message.delete()
        await callback.message.answer(LEXICON["reg_teacher_selected"], reply_markup=default_kb)
        await callback.answer()
        await state.clear()


@router.message(F.text.lower() == "регистрация")
async def registration(msg: Message) -> None:
    with Session(engine) as session:
        res = session.execute(select(Chat).where(Chat.id == msg.chat.id))
        existing_chat = res.first()

        if not existing_chat:
            main_logger.info(f"New chat! ID: {msg.chat.id}, type: {msg.chat.type}")
            match msg.chat.type:
                case "private":
                    session.add(Chat(id=msg.chat.id, kind="private", name=msg.from_user.full_name, username=msg.from_user.username))
                    session.commit()
                case _:
                    session.execute(Chat(id=msg.chat.id, kind="group", name=msg.chat.title))
                    session.commit()
        else:
            main_logger.info(f"Chat already exists! ID: {msg.chat.id}, type: {msg.chat.type}")

    await msg.answer(LEXICON["reg_group_or_teacher"], reply_markup=reg_group_or_teacher_kb)


@router.callback_query(F.data == "reg_cancel")
async def process_callback_exit(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text( LEXICON["reg_cancel"])



### other

@router.message(F.text.lower().startswith('пары'))
async def handle_lessons(msg: Message, tokens: List[str]):
    processed = process_lessons_tokens(tokens)
    # processed ['lessons', 'teacher', '1' (api_id), '21.09.24']

    # request from api
    # transform request to message
    # send message
    result = "not implemented yet"
    await msg.answer(result)

@router.message(F.text.lower().startswith('помощь'))
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
