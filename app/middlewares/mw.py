import re
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.orm import Session

from app.database import Chat, engine
from app.database.operations import find_admin
from app.exceptions import ( AdminLevelError, StudyEntityNotFoundError, StudyEntityNotSelectedError, WrongStudyEntityKindError,)
from app.logic import extract_lessons_tokens
from app.shared import ADMIN_LEXICON, LEXICON, command_tokens, main_logger


# Checks if a chat is banned. If it is, breaks the middleware chain
class ValidateMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()

    async def __call__( self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any],) -> Any:
        if event.message:
            chat = event.message.chat
        # elif event.edited_message:
        #     chat = event.edited_message.chat
        elif event.callback_query:
            chat = event.callback_query.message.chat
        else:
            # If the update doesn't contain a message, stop processing
            return

        with Session(engine) as session:
            this_chat = session.query(Chat).filter(Chat.id == chat.id).first()
            if not this_chat:
                return await handler(event, data)
            elif this_chat.is_banned:
                return

        return await handler(event, data)


class LoggingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()

    async def __call__( self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any],) -> Any:
        if event.text:
            first_word = event.text.split(" ")[0].lower()
            if first_word in command_tokens:
                match event.chat.type:
                    case "private":
                        log = f"{str(event.from_user.full_name)} in @{str(event.chat.username)} ({str(event.chat.id)}): {str(event.text)}"
                    case _:
                        log = f"{str(event.from_user.full_name)} in {str(event.chat.title)} ({str(event.chat.id)}): {str(event.text)}"
                main_logger.telegram(log)

        result = await handler(event, data)

        # with Session(engine) as session:
        #     this_chat = session.query(Chat).filter(Chat.id == event.chat.id).first()
        # TODO: make db syncing
        return result


class TokenizerMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()

    async def __call__( self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any],) -> Any:
        if event.text:
            text = re.sub(" +", " ", event.text).lower().strip()
            split_words = text.split(" ")
            while (len(split_words)) < 10:
                split_words.append("")
            command_token = split_words[0]
            match command_token:
                case "пары":
                    tokens = extract_lessons_tokens(split_words)
                case _:
                    tokens = split_words

            data["tokens"] = tokens

        return await handler(event, data)


class ErrorHandlingMiddleware(BaseMiddleware):
    async def __call__( self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any],):
        try:
            return await handler(event, data)
        except WrongStudyEntityKindError as e:
            main_logger.error(e.__str__())
            await event.reply(LEXICON["exception"])
        except StudyEntityNotFoundError as e:
            main_logger.error(e.__str__())
            await event.reply(LEXICON["exception"])
        except StudyEntityNotSelectedError as e:
            main_logger.error(e.__str__())
            await event.reply(LEXICON["err_se_not_selected"])
        except AdminLevelError as e:
            main_logger.error(e.__str__)
            await event.reply(ADMIN_LEXICON["not_enough_rights"])
        except BaseException as e:
            main_logger.error(e)
            await event.reply(LEXICON["exception"])


class AdminCheckMiddleware(BaseMiddleware):
    async def __call__( self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any],):
        with Session(engine) as session:
            admin = find_admin(event.from_user.id)
            if admin:
                data["level"] = admin.level
                return await handler(event, data)
