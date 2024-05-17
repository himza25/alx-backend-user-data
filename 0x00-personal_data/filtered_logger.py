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
    """
    Connect to secure database
    """
    DB_USERNAME = getenv("PERSONAL_DATA_DB_USERNAME", "root")
    DB_PASSWORD = getenv("PERSONAL_DATA_DB_PASSWORD", "")
    DB_HOST = getenv("PERSONAL_DATA_DB_HOST", "localhost")
    DB_NAME = getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        database=DB_NAME
    )


def main() -> None:
    """
    Read and filter
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names
    for row in cursor:
        message = ""
        for i in range(len(fields)):
            message += f"{fields[i]}={row[i]};"
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
