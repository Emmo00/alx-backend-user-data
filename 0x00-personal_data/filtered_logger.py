#!/usr/bin/env python3
"""
filter logger module
"""
import re
from typing import List
import logging
import mysql.connector
from os import getenv

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
    custom_log = logging.getLogger('user_data')
    custom_log.setLevel(logging.INFO)
    custom_log.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    custom_log.addHandler(stream_handler)
    return custom_log


def get_db() -> mysql.connector.connection.MySQLConnection:
    return mysql.connector.connect(host=getenv('PERSONAL_DATA_DB_HOST'),
                                   user=getenv('PERSONAL_DATA_DB_USERNAME'),
                                   password=getenv('PERSONAL_DATA_DB_PASSWORD'),
                                   database=getenv('PERSONAL_DATA_DB_NAME'))
