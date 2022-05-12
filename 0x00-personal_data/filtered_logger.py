#!/usr/bin/env python3
"""Module Regex-ing"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns log message"""
    tempMessage = message
    for field in fields:
        tempMessage = re.sub(field + "=.*?" + separator,
                             field + "=" + redaction + separator, tempMessage)
    return tempMessage
