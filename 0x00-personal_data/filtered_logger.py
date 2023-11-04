#!/usr/bin/env python3
"""
filter logger module
"""
import re
from typing import List


def filter_datum(fields: List, redaction: str, message: str, separator: str) -> str:
    for field in fields:
        pattern = fr'({re.escape(field)})=.+?{separator}'
        message = re.sub(pattern, fr'\1={redaction}{separator}', message)
    return message
