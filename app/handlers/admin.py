from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from app.shared import dp, bot, main_logger, admin_ids
from app.database import Chat, engine

admin_router = Router()


@admin_router.message(Command("kill"))
async def cmd_kill(message: Message) -> None:
    if not (message.from_user.id in admin_ids):
        pass

    await message.reply("Я умер")
    await dp.stop_polling()

# FIXME: по-нормальному переписать. щас лень чето
@admin_router.message(Command("send"))
async def cmd_send(msg: Message, tokens: List[str]) -> None:
    if not (msg.from_user.id in admin_ids):
        pass

    text = msg.text
    while len(text.split(" ")) < 3:
        text += " ."

    if tokens[2] == "":
        await msg.reply("Сообщение пусто!")
        return
    address_id = text.split(" ")[1]
    sent_msg = text.split(" ", 2)[2]
    try:
        await bot.send_message(address_id, sent_msg)
        await msg.reply("Отправлено")
    except Exception as e:
        main_logger.error(e)
        await msg.reply("Не получилось отправить")

@admin_router.message(Command("send_all"))
async def cmd_send_all(msg: Message, tokens: List[str]) -> None:
    if not (msg.from_user.id in admin_ids):
        pass

    text = msg.text
    while len(text.split(" ")) < 2:
        text += " ."
    sent_msg = text.split(" ", 1)[1]

    if tokens[2] == "":
        await msg.reply("Сообщение пусто!")
        return

    ids = []
    with Session(engine) as session:
        chats = session.query(Chat).all()

        for chat in chats:
            ids.append(chat.id)

    successful = 0
    failed = 0
    for id in ids:
        try:
            await bot.send_message(id, sent_msg)
            successful += 1
        except:
            failed += 1

    await msg.reply(
        "Отправлено (всего: "
        + str(len(ids))
        + ", успешно: "
        + str(successful)
        + ", неудачно: "
        + str(failed)
        + ")"
    )
    # try:
    #     await bot.send_msg(address_id, msg, parse_mode=ParseMode.HTML)
    #     await msg.reply("Отправлено")
    # except Exception as e:
    #     await msg.reply("Не получилось отправить")
