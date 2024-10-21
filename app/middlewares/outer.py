from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from utils import main_logger


class LoggingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.message:
            if event.message.text:
                match event.message.chat.type:
                    case 'private':
                        log = f"{str(event.message.from_user.full_name)} in @{str(event.message.chat.username)} ({str(event.message.chat.id)}): {str(event.message.text)}"
                    case _:
                        log = f"{str(event.message.from_user.full_name)} in {str(event.message.chat.title)} ({str(event.message.chat.id)}): {str(event.message.text)}"
            main_logger.telegram(log)
        result = await handler(event, data)
        return result

class TokenizerMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.message:
            if event.message.text:
                tokens = str.lower(event.message.text.strip()).split(' ')
                while(len(tokens)) < 10:
                    tokens.append('')
                data['tokens'] = tokens
        result = await handler(event, data)
        return result
