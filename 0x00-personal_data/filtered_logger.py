#!/usr/bin/env python3
"""
This module provides functions to obfuscate specific fields in log messages.
"""

import re
import logging
from typing import List, Tuple

# Define PII_FIELDS at the root of the module
PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone_number",
                               "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscates fields in a log message.

    Args:
        fields (List[str]): Fields to obfuscate.
        redaction (str): Obfuscation string.
        message (str): Log line.
        separator (str): Field separator.

    Returns:
        str: Obfuscated log message.
    """
    pattern = '|'.join([f'{field}=[^{separator}]*' for field in fields])
    return re.sub(pattern, lambda m: f'{m.group(0).split("=")[0]}={redaction}',
                  message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record by obfuscating specified fields.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted and obfuscated log record.
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, original_message,
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger object.

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger
