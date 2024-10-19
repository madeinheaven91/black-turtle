from environs import Env

from dataclasses import dataclass


@dataclass
class TgBot:
    token: str

@dataclass
class Db:
    name: str
    user: str
    password: str
    port: int
    host: str

    def __post_init__(self):
        self.url = f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'

@dataclass
class Config:
    bot: TgBot
    db: Db

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env()
    return Config(
        bot=TgBot(
            token=env('BOT_TOKEN')
        ),
        db=Db(
            host=env('POSTGRES_HOST'),
            name=env('POSTGRES_NAME'),
            user=env('POSTGRES_USER'),
            password=env('POSTGRES_PASSWORD'),
            port=env('POSTGRES_PORT')
        )
    )
