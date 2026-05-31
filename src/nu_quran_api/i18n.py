import re
from typing import Optional

from django.utils.translation import gettext as _


class DynamicErrorTranslator:
    _ERROR_STRINGS: list[tuple[str, str]] = [
        (
            r"^No (?P<model>[a-zA-Z]+) matches the given query\.$",
            "No %(model)s matches the given query.",
        )
    ]

    def translate(self, msg: str) -> str:
        # NOTE: Fallback to literal translation
        translated: str = _(msg)

        for regex, msgid in self._ERROR_STRINGS:
            match: Optional[re.Match] = re.fullmatch(regex, msg)
            if match:
                placeholders: set[str] = set(match.groupdict().keys()).difference(
                    ("default",)
                )

                # NOTE: Translate the message with placeholders set for each match group
                # Example:
                # msg = "No user matches the given query."
                # regex = r"^No (?P<model>[a-zA-Z]+) matches the given query\.$"
                # msgid = "No %(model)s matches the given query."
                # match groups = {"model": "user"}
                # placeholders = { "model" }
                # translated = _("No %(model)s matches the given query.") % { "model": _("user") }
                translated = _(msgid) % {
                    placeholder: _(match.group(placeholder))
                    for placeholder in placeholders
                }
                break

        return translated
