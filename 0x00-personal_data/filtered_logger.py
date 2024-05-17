#!/usr/bin/env python3
"""
This module provides functions to obfuscate log messages.
"""

import re
import logging
from typing import List, Tuple
import os
import mysql.connector

PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscates fields in a log message."""
    pattern = '|'.join([f'{field}=[^{separator}]*' for field in fields])
    return re.sub(pattern, lambda m: f'{m.group(0).split("=")[0]}={redaction}',
                  message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats log record by obfuscating specified fields."""
        original = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original,
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Creates and returns a logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database."""
    return mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )


def main() -> None:
    """Obtains a DB connection and retrieves all rows in the users table."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        message = ("name={}; email={}; phone={}; ssn={}; password={};"
                   " ip={}; last_login={}; user_agent={};").format(*row)
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
