#!/usr/bin/env python3
"""
filter logger module
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    for field in fields:
        message = re.sub(r"(?<={}=)[^{}]*(?={})".format(field,
                                                        separator, separator),
                         redaction, message)
    return message
