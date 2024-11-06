from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from typing import List
from enum import Enum
from app.exceptions import AdminLevelError
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from app.shared import dp, bot, ADMIN_LEXICON, main_logger
from app.database import Chat, engine, Admin

admin_router = Router()

class Levels(Enum):
    OWNER = 5
    SEN_ADMIN = 4
    JUN_ADMIN = 3
    SEN_MODER = 2
    JUN_MODER = 1

# FIXME: doesnt work
@admin_router.message(Command("kill"))
async def cmd_kill(msg: Message, level: int) -> None:
    if level <  Levels.OWNER.value:
        raise AdminLevelError("Not enough rights to execute this command")

    await msg.reply("Я умер")
    await bot.close()
    await dp.storage.close()
    await dp.stop_polling()

@admin_router.message(Command("send"))
async def cmd_send(msg: Message, level: int, tokens: List[str]) -> None:
    if level <  Levels.JUN_ADMIN.value:
        raise AdminLevelError("Not enough rights to execute this command")

    if not msg.reply_to_message:
        await msg.reply(ADMIN_LEXICON["msg_not_selected"])
        return ## FIXME: сделать экзепшн для отлавливания такого случая

    if not tokens[1]:
        raise # FIXME: сделать экзепшн для случая когда не указан адресат

    address_id = tokens[1]

    try:
        await bot.copy_message(chat_id=address_id, from_chat_id=msg.chat.id, message_id=msg.reply_to_message.message_id)
    except:
        raise

@admin_router.message(Command("send_all"))
async def cmd_send_all(msg: Message, level: int) -> None:
    if level <  Levels.SEN_ADMIN.value:
        raise AdminLevelError("Not enough rights to execute this command")

    if not msg.reply_to_message:
        await msg.reply(ADMIN_LEXICON["msg_not_selected"])
        return

    with Session(engine) as session:
        chats = session.query(Chat).all()

    failed = []

    for chat in chats:
        try:
            await bot.copy_message(chat_id=chat.id, from_chat_id=msg.chat.id, message_id=msg.reply_to_message.message_id)
        except:
            failed.append(chat)
            main_logger.error("Failed to send message to " + str(chat.id)) 

    res = f"<b>Отправлено (всего: {str(len(chats))}, успешно: {str(len(chats) - len(failed))} неудачно: {str(len(failed))})</b>\n\nНеудачные:"
    for f in failed:
        res += f"\n{f.id}, {f.name}"

    await msg.reply(res)

@admin_router.message(Command("ban"))
async def cmd_ban(msg: Message, level: int, tokens: List[str]) -> None:
    if level <  Levels.JUN_ADMIN.value:
        raise AdminLevelError("Not enough rights to execute this command")
    if not tokens[1]:
        raise # FIXME: сделать экзепшн для случая когда не указан адресат

    address_id = tokens[1]
    with Session(engine) as session:
        chat = session.query(Chat).filter(Chat.id == address_id).first()
        admin = session.query(Admin).filter(Admin.id == address_id).first()

        if not chat:
            await msg.reply(f"Чат (id: {address_id}) не найден!")
            return
        if admin and admin.level >= level:
            await msg.reply(ADMIN_LEXICON["cant_ban_higher_admin"])
            return

        chat.is_banned = True
        session.expunge_all()
        session.commit()
    await msg.reply(f"Чат '{chat.name}' (id: {chat.id}) забанен")

@admin_router.message(Command("unban"))
async def cmd_unban(msg: Message, level: int, tokens: List[str]) -> None:
    if level <  Levels.JUN_ADMIN.value:
        raise AdminLevelError("Not enough rights to execute this command")
    if not tokens[1]:
        raise # FIXME: сделать экзепшн для случая когда не указан адресат

    address_id = tokens[1]
    with Session(engine) as session:
        chat = session.query(Chat).filter(Chat.id == address_id).first()
        admin = session.query(Admin).filter(Admin.id == address_id).first()

        if not chat:
            await msg.reply(f"Чат (id: {address_id}) не найден!")
            return
        if admin:
            if admin.level >= level:
                await msg.reply(ADMIN_LEXICON["cant_ban_higher_admin"])
                return
        chat.is_banned = False
        session.expunge_all()
        session.commit()
    await msg.reply(f"Чат '{chat.name}' (id: {chat.id}) разбанен")

# TODO: promote and demote cmds
# also stat cmd

# @admin_router.message(Command("promote"))
# async def cmd_promote(msg: Message, level: int, tokens: List[str]) -> None:
#     if level <  Levels.OWNER.value:
#         raise AdminLevelError("Not enough rights to execute this command")
#     if not tokens[1]:
#         raise # FIXME: сделать экзепшн для случая когда не указан адресат
#
#     address_id = tokens[1]
#     rank = tokens[2]
#
#     with Session(engine) as session:
#         chat = session.query(Chat).filter(Chat.id == address_id).first()
#         if not chat:
#             await msg.reply(f"Чат (id: {chat.id}) не найден!")
#             return

@admin_router.message(Command("stat"))
async def cmd_stat(msg: Message):
    with Session(engine) as session:
        chats = session.query(Chat).all()
        groups = session.query(Chat).filter(Chat.kind == "group").all()
    res = f"<b>Всего чатов: {str(len(chats))}</b>\nЛичных чатов: {str(len(chats) - len(groups))}\nГрупп: {str(len(groups))}"
    await msg.reply(res)
