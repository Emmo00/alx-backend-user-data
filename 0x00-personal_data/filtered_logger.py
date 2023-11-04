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
        pattern = f'{field}=.+{separator}([a-zA-Z$])'
        repl = f'{field}={redaction}{separator}\0'
        message = re.sub(pattern, repl, message)
    return message
