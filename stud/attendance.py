from flask import Blueprint, render_template, session, flash, redirect, url_for
from db import connect_test1

# Create a Flask Blueprint for student dashboard
student_bp = Blueprint('student', __name__, template_folder='../templates')

# -----------------------------
# Database Connection Function
# -----------------------------
def get_db_connection():
    return connect_test1()

# -----------------------------
def get_day_student_per(username):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT status, COUNT(*) as count
                FROM day_attendance
                WHERE username = %s
                GROUP BY status
            """
            cursor.execute(sql, (username,))
            day_rec = cursor.fetchall()

            return day_rec
    finally:
        conn.close()
# Fetch Attendance Function
# -----------------------------
def get_day_student_attendance(username):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT id,date,status
                FROM day_attendance
                WHERE username = %s
                order by date desc
            """
            cursor.execute(sql, (username,))
            day_record = cursor.fetchall()

            return day_record
    finally:
        conn.close()

def get_student_attendance(username):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT username, percent
                FROM attendance
                WHERE username = %s
            """
            cursor.execute(sql, (username,))
            records = cursor.fetchall()

            return records
    finally:
        conn.close()

# -----------------------------
# Student Dashboard Route
# -----------------------------
@student_bp.route('/student_attendance')
def student_attendance():
    # Check session (only allow logged-in students)
    if 'username' not in session or session.get('role') != 'student':
        flash("Access denied! Please log in as a student.", "danger")
        return redirect(url_for('login'))  # Use your main login route

    username = session['username']  # Retrieve logged-in student username
    attendance_records = get_student_attendance(username)
    day_attendance_records = get_day_student_attendance(username)
    percent_rec=get_day_student_per(username)

    attendance = {'Present': 0, 'Absent': 0, 'Leave': 0}
    for row in percent_rec:
        attendance[row['status']] = row['count']

    return render_template(
        "attendance.html",
        username=username,
        attendance2=day_attendance_records,
        attendance=attendance
    )

