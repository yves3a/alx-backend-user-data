#!/usr/bin/env python3


"""This module defines the `filter_datum` function."""

import logging
import os
import re
from typing import List

from mysql.connector import errors
from mysql.connector.connection import MySQLConnection

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Redact specified fields in a log message."""
    pattern = (
        rf"({'|'.join(map(re.escape, fields))})=([^\s{re.escape(separator)}]*)"
    )
    return re.sub(pattern, rf"\1={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize logger."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values coming from log records."""
        record.msg = filter_datum(
            fields=self.fields,
            redaction=self.REDACTION,
            message=record.msg,
            separator=self.SEPARATOR,
        )
        return super(RedactingFormatter, self).format(record=record)


def get_logger() -> logging.Logger:
    """
    Return a logger object for user data.

    Returns:
        logging.Logger: A logger object for handling user data logs.
    """
    logger = logging.getLogger(name="user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """Return a database connection."""
    try:
        return MySQLConnection(
            user=os.environ.get("PERSONAL_DATA_DB_USERNAME", "root"),
            password=os.environ.get("PERSONAL_DATA_DB_PASSWORD", ""),
            host=os.environ.get("PERSONAL_DATA_DB_HOST", "localhost"),
            database=os.environ.get("PERSONAL_DATA_DB_NAME"),
        )
    except errors.ProgrammingError as e:
        logging.error(f"Database connection failed - {e.msg}")


def main() -> None:
    """Connect to the database and print all rows of the users table."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    [print(row) for row in cursor.fetchall()]
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
