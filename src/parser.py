import copy
from loguru import logger
from src import constants
from src.constants import Dividers
from src.rule import Rule


class Parser:
    """Parses file to extract rules"""

    rules: list[Rule]
    divider: Dividers
    verbose: bool

    def __init__(self, verbose: bool = False):
        self.divider = Dividers.NOT_SET
        self.verbose = verbose

    def parse_divider(self, strings: list[str]) -> bool:
        """Gets strings without comments and updates divider

        Args:
            strings (list[str]): program code

        Returns:
            bool: was divider found correctly
        """

        for s in strings:
            if s.startswith("divider"):
                tokens = s.split("=")

                if len(tokens) != 2:
                    if self.verbose:
                        logger.error(
                            "wrong divider format (or using reserved divider string)"
                        )
                    return False

                divider_type = tokens[-1].strip()
                # check if divider_type is correct
                if divider_type not in constants.ALLOWED_DIVIDERS:
                    if self.verbose:
                        logger.error(
                            f"unknown divider type '{divider_type}', "
                            f"allowed: {constants.ALLOWED_DIVIDERS}"
                        )

                    return False

                new_divider = constants.DIVIDER_TO_ENUM[divider_type]
                # check if self.divider is already set to different divider
                if self.divider is not Dividers.NOT_SET and self.divider != new_divider:
                    if self.verbose:
                        logger.error("different dividers found in code")

                    return False

                # updating divider
                self.divider = new_divider

        # default divider value
        if self.divider is Dividers.NOT_SET:
            self.divider = Dividers.NONE

        if self.verbose:
            logger.info(f"divider set to {self.divider}")

        return True

    def parse_rules(self, strings: list[str]) -> bool:
        """Gets strings without comments and updates rules

        Args:
            strings (list[str]): program code

        Returns:
            bool: was rules set correctly
        """

        if self.divider is Dividers.NOT_SET:
            if self.verbose:
                logger.error("call of parse_rules() while divider is not set")
            raise RuntimeError("call of parse_rules() while divider is not set")

        found_rules: list[Rule] = []
        for s in strings:
            if not s.startswith("divider"):
                rule_splitted = s.split("->")
                if len(rule_splitted) != 2:
                    if self.verbose:
                        logger.error(f"found wrong line in code: '{s}'")
                    return False

                original_s = rule_splitted[0]
                replace_s = rule_splitted[1]

                def _split(string: str):
                    if self.divider is Dividers.NONE:
                        splitted = list(string)
                    else:
                        splitted = [token.strip() for token in string.split(" ")]

                    cleared: list[str] = []
                    for token in splitted:
                        if token not in " \t\n":
                            cleared.append(token)

                    return cleared

                original = _split(original_s)
                replace = _split(replace_s)

                found_rules.append(Rule(original, replace))

        self.rules = found_rules
        if self.verbose:
            logger.info(f"found {len(found_rules)} rules")

        return True

    def update_from_strings(self, strings: list[str]) -> bool:
        """Updates rules and divider with program code

        Args:
            strings (list[str]): program code

        Returns:
            bool: was the parsing ok
        """

        without_comments: list[str] = []

        # removing empty string and comments
        for s in strings:
            s = s.strip(" \t\n")
            if len(s) and s[0] != constants.COMMENT_CHARACTER:
                comment_begin = s.find(constants.COMMENT_CHARACTER)
                if comment_begin == -1:
                    comment_begin = len(s)

                without_comments.append(s[:comment_begin].strip(" \t\n"))

        # finding divider
        divider_parse_result = self.parse_divider(without_comments)

        # check if found with errors
        if not divider_parse_result:
            return False

        rules_parse_result = self.parse_rules(without_comments)
        if not rules_parse_result:
            return False

        if self.verbose:
            logger.success(f"parsed {len(self.rules)} rules")

        return True

    def update_from_file(self, path: str) -> bool:
        """Reads file and updates self

        Args:
            path (str): path to file

        Returns:
            bool: was the parsing ok
        """

        with open(path, "r", encoding="utf-8") as f:
            return self.update_from_strings(f.readlines())

    def get_rules(self) -> list[Rule]:
        """Returns list of parsed rules"""
        return copy.deepcopy(self.rules)
