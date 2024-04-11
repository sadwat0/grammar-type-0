from src.constants import Dividers


def state_to_string(state: list[str], divider: Dividers) -> str:
    """Converts state to printable string according to divider"""

    match divider:
        case Dividers.NONE:
            return "".join(state)
        case Dividers.SPACES:
            return ", ".join(state)
        case Dividers.NOT_SET:
            raise ValueError("divider not set")
