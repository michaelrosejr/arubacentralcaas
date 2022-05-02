import sys
from pathlib import Path

from loguru import logger

WORK_DIR = Path(__file__).parents[2]
sys.path.append(str(WORK_DIR / "arubacentralcaas/arubacentralcaas"))
sys.path.append(str(WORK_DIR / "arubacentralcaas"))

from .config.settings import log_level  # noqa: E402

logger.remove()


class LogFilter:
    def __init__(self, level):
        self.level = level

    def __call__(self, record):
        levelno = logger.level(self.level).no
        return record["level"].no >= levelno


log_filter = LogFilter(log_level)  # type: ignore

logger.add(
    sys.stderr,
    colorize=True,
    filter=log_filter,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <blue>{level}</blue> |"
    " <cyan>{name}:{function}:{line}</cyan> | <bold><level>{message}</level></bold>",
    level=0,
)
