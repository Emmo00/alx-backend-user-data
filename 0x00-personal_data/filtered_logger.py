#!/usr/bin/env python3
"""
filter logger module
"""
import re
from typing import List, Iterable
import logging

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initialize formatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format message log"""
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """filter datum"""
    for field in fields:
        message = re.sub(r"(?<={}=)[^{}]*(?={})".format(field,
                                                        separator, separator),
                         redaction, message)
    return message


def get_logger() -> logging.Logger:
    """ return a custom logger """
    custom_log = logging.Logger('user_data', logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    custom_log.addHandler(stream_handler)
    return custom_log
