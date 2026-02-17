"""Centralized database utilities.

This module exports a single `connect` function and convenience wrappers for
each of the four databases used in the application.  It keeps connection
parameters in one place so that the rest of the project can simply do

    from db import connect
    conn = connect('test1')

or one of the helper functions like `connect_test1()`.

The implementation uses the same credentials that were scattered throughout
the code.  Changing the host/user/password in future only requires editing this
file; the shape of the interface remains constant so the existing modules do
not need to be restructured.  No database structure or routing is modified.
"""

import pymysql
import mysql.connector
from typing import Any, Dict

# central config; you may override via environment variables
BASE_CONFIG: Dict[str, Any] = {
    "host": "localhost",
    "user": "root",
    "password": "masterarun1",
}


def connect(db_name: str, **kwargs) -> Any:
    """Return a connection object for the requested database.

    The function picks between pymysql and mysql.connector based on the
    database name (mysql.connector is used for `payments_db` and
    `hostel_mgmt` where some code relied on the `dictionary=True` option).
    Additional connection kwargs are forwarded to the underlying connector.
    """
    config = {**BASE_CONFIG, **kwargs}
    config["database"] = db_name

    if db_name in ("payments_db", "hostel_mgmt"):
        # use mysql.connector for these schemas (some modules already imported it)
        return mysql.connector.connect(**config)
    else:
        return pymysql.connect(cursorclass=pymysql.cursors.DictCursor, **config)


def connect_test1() -> Any:
    return connect("test1")


def connect_payments() -> Any:
    return connect("payments_db")


def connect_details() -> Any:
    return connect("details")


def connect_hostel() -> Any:
    return connect("hostel_mgmt")
