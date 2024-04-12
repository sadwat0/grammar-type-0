"""Constants module"""

import enum


class Dividers(enum.Enum):
    """Enum for divider types"""

    NOT_SET = 0
    NONE = 1
    SPACES = 2


LOGGER_FORMAT = "<level>{level: <8}</level> | <level>{message}</level>"
STEPS_LIMIT = 10_000
COMMENT_CHARACTER = "#"

DIVIDER_TO_ENUM = {"none": Dividers.NONE, "spaces": Dividers.SPACES}
ALLOWED_DIVIDERS = list(DIVIDER_TO_ENUM.keys())
