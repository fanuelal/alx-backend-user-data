#!/usr/bin/env python3
"""Module Regex-ing"""
import re
from typing import List
import logging
from mysql.connector import connection
from os import environ


PII_FIELDS = ('name', 'email', 'password', 'snn', 'phone')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns log message"""
    tempMessage = message
    for field in fields:
        tempMessage = re.sub(field + "=.*?" + separator,
                             field + "=" + redaction + separator, tempMessage)
    return tempMessage


def get_logger() -> logging.Logger:
    """Returns logging of logger"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logging.propagate = False
    stream_Handler = logging.StreamHandler()
    stream_Handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_Handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """connect to the db"""
    dbUser = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    dbPassword = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    dbHost = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    dbName = environ.get("PERSONAL_DATA_DB_NAME")
    connect = connection.MySQLConnection(
        user = dbUser,
        password = dbPassword,
        host = dbHost,
        name = dbName)
    return connect

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format method to filter"""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)
