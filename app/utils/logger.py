from datetime import datetime
import logging
from logging import Formatter, Logger
from config import load_config

conf = load_config()

# Add TELEGRAM log level and a method to log telegram-level messages
TELEGRAM = 25
logging.addLevelName(TELEGRAM, "TELEGRAM")
def telegram(self, message, *args, **kws):
    if self.isEnabledFor(TELEGRAM):
        self._log(TELEGRAM, message, args, **kws)
logging.Logger.telegram = telegram


def init_logger(level: int | str, formatter: Formatter) -> Logger:
    match level:
        case "DEBUG" | 10:
            log_level = logging.DEBUG
        case "TELEGRAM" | 25:
            log_level = TELEGRAM
        case "WARNING" | 30:
            log_level = logging.WARNING
        case "ERROR" | 40:
            log_level = logging.ERROR
        case "CRITICAL" | 50:
            log_level = logging.CRITICAL
        case _: 
            log_level = logging.INFO

    filename = f'./logs/{datetime.now().strftime("%Y-%m-%d")}.log'
    file = open(filename, 'a')
    file.close()
    fh = logging.FileHandler(filename)
    fh.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(fh)
    
    return logger


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d | %H:%M:%S",
)
main_formatter = Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d | %H:%M:%S")
main_logger = init_logger(conf.app.log_level, main_formatter)
