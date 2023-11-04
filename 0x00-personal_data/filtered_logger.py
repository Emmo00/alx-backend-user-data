#!/usr/bin/env python3
"""
filter logger module
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    filter datum
    """
    for field in fields:
        print(message)
        pattern = fr'({re.escape(field)})=.+?{separator}'
        repl = fr'\1={redaction}{separator}'
        message = re.sub(pattern, repl, message)
    return message
