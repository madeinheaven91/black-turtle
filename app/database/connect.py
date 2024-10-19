from config import config
from sqlalchemy import create_engine

conf = config.load_config()

engine = create_engine(conf.db.url)
