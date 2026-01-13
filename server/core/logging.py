import logging
import sys
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

LEVEL_COLORS = {
    logging.DEBUG: Fore.CYAN,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.RED + Style.BRIGHT,
}


class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        color = LEVEL_COLORS.get(record.levelno, "")
        levelname = f"{color}{record.levelname}{Style.RESET_ALL}"

        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")

        return (
            f"{timestamp} | "
            f"{levelname:<8} | "
            f"{record.name}:{record.lineno} | "
            f"{record.getMessage()}"
        )


def setup_logging(environment: str) -> None:
    level = logging.DEBUG if environment != "production" else logging.INFO

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(ColorFormatter())

    root = logging.getLogger()
    root.setLevel(level)

    root.handlers.clear()
    root.addHandler(handler)

    logging.getLogger("uvicorn").handlers.clear()
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
