from typing import Any, Awaitable, Callable, Dict
import re

from aiogram import BaseMiddleware
from aiogram.types import Message
from logic import extract_lessons_tokens
from shared import main_logger, command_tokens
from database import engine, Chat
from sqlalchemy.orm import Session

# Checks if a chat is banned. If it is, breaks the middleware chain 
class ValidateMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.message:
            chat = event.message.chat

        with Session(engine) as session:
            this_chat = session.query(Chat).filter(Chat.id == chat.id).first()
            if this_chat.is_banned:
                return

        return await handler(event, data)

class LoggingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.text:
            first_word = event.text.split(" ")[0].lower()
            if not (first_word in command_tokens):
                return
            match event.chat.type:
                case 'private':
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

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.text:
            text = re.sub(' +', ' ', event.text).lower().strip()
            split_words = text.split(' ')
            while(len(split_words)) < 10:
                split_words.append('')
            command_token = split_words[0]
            match command_token:
                case "пары":
                    tokens = extract_lessons_tokens(split_words)
                case _:
                    tokens = split_words

            data['tokens'] = tokens

        return await handler(event, data)
