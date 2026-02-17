"""Database initialization helper.

This module defines functions that ensure the required MySQL databases and tables
exist before the application starts.  It's safe to import and call from
`login.py` at startup; each `CREATE ... IF NOT EXISTS` statement will simply
no-op if the object already exists.

The `Data base` folder contains dump files that document the current structure
of each schema.  The code below mirrors those definitions and provides a
programmatic way to create them.
"""

import pymysql
import mysql.connector

# root-level connection options (used to create databases)
ROOT_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "masterarun1",
}


def ensure_database(db_name: str):
    """Create a database if it does not already exist."""
    conn = pymysql.connect(**ROOT_CONFIG)
    with conn.cursor() as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
    conn.commit()
    conn.close()


def init_test1():
    ensure_database("test1")
    conn = pymysql.connect(database="test1", **ROOT_CONFIG)
    cur = conn.cursor()
    # users table used for authentication
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            password VARCHAR(255),
            role VARCHAR(255)
        )
        """
    )
    # stored messages from admin/staff to students
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS query_messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender VARCHAR(255),
            student_username VARCHAR(255),
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    # marks table referenced by name, additional columns may be added by hand
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ca1 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255)
            -- additional mark/subject columns can be added later
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS attendance (
            username VARCHAR(255),
            percent FLOAT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS day_attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            date DATE,
            status VARCHAR(50),
            username VARCHAR(255)
        )
        """
    )
    # google_forms also exists in test1 (some modules may refer to it)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS google_forms (
            id INT AUTO_INCREMENT PRIMARY KEY,
            form_name VARCHAR(255),
            form_id VARCHAR(255),
            sheet_id VARCHAR(255),
            sheet_url VARCHAR(255)
        )
        """
    )
    conn.commit()
    conn.close()


def init_payments_db():
    ensure_database("payments_db")
    conn = mysql.connector.connect(database="payments_db", **ROOT_CONFIG)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS payments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            stud_id INT,
            amount FLOAT,
            payment_id VARCHAR(255),
            status VARCHAR(50)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS fees (
            stud_id INT PRIMARY KEY,
            amount FLOAT
        )
        """
    )
    conn.commit()
    conn.close()


def init_details_db():
    ensure_database("details")
    conn = pymysql.connect(database="details", **ROOT_CONFIG)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS google_forms (
            id INT AUTO_INCREMENT PRIMARY KEY,
            form_name VARCHAR(255),
            form_id VARCHAR(255),
            sheet_id VARCHAR(255),
            sheet_url VARCHAR(255)
        )
        """
    )
    # other tables are created dynamically by the import routines
    conn.commit()
    conn.close()


def init_hostel_db():
    ensure_database("hostel_mgmt")
    conn = mysql.connector.connect(database="hostel_mgmt", **ROOT_CONFIG)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            email VARCHAR(255)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS rooms (
            id INT AUTO_INCREMENT PRIMARY KEY,
            room_no VARCHAR(255),
            floor INT,
            capacity INT,
            available INT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS allocations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            room_id INT,
            allocated_at DATETIME
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS payments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            status VARCHAR(50),
            student_id INT,
            amount FLOAT,
            txn_id VARCHAR(255)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS fees (
            stud_id INT PRIMARY KEY,
            amount FLOAT
        )
        """
    )
    conn.commit()
    conn.close()


def initialize_all():
    """Convenience function called at startup."""
    init_test1()
    init_payments_db()
    init_details_db()
    init_hostel_db()


if __name__ == "__main__":
    initialize_all()
