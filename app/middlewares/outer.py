from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from utils.logger import logger

class LoggingMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.counter = 0

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logger.info(str(event.message.text))
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
        tokens = str.lower(event.message.text.strip()).split(' ')
        while(len(tokens)) < 10:
            tokens.append('')

        data['tokens'] = tokens
        result = await handler(event, data)
        return result
