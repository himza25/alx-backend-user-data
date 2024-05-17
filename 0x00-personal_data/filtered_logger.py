#!/usr/bin/env python3
"""
This module provides a function to obfuscate specific fields in log messages.
"""

import re
from typing import List


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
