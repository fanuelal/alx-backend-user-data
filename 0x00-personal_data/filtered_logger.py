#!/usr/bin/env python3
"""Module Regex-ing"""
import logging
import re

def filter_datum(fields, redaction, message, separator):
    """returns log message"""
    tempMessage = message
    for field in fields:
        tempMessage = re.sub(field + "=.*?" + separator,
                      field + "=" + redaction + separator, tempMessage)
    return tempMessage
