from flask import Blueprint, render_template, session, flash, redirect, url_for
from db import connect_test1, connect_payments
from stud.attendance import get_student_attendance

# Blueprint for student dashboard
studentatt_bp = Blueprint('stud', __name__, template_folder='../templates')

# -----------------------------
# Database connection
# -----------------------------
def get_db_connection():
    return connect_test1()

def get_pay_db():
    return connect_payments()
# -----------------------------

# Fetch attendance for studen
def get_stud_mark(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ca1 WHERE name=%s", (username,))
    student_mark = cursor.fetchone()
    cursor.close()
    return student_mark

def get_percent(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT percent FROM attendance WHERE username=%s", (username,))
    percent = cursor.fetchone()
    cursor.close()
    return percent




# -----------------------------
# Fetch messages sent to student
# -----------------------------
def get_student_messages(username):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT id,sender, message, created_at
                FROM query_messages
                WHERE student_username=%s
                ORDER BY created_at DESC
            """
            cursor.execute(sql, (username,))
            messages = cursor.fetchall()
            return messages
    finally:
        conn.close()

# -----------------------------
# Student dashboard route
# -----------------------------
@studentatt_bp.route('/student_dashboard')
def student_dashboard():
    # Check if logged in and is student
    username = session.get('username')
    user_id=session.get('id')
    role = session.get('role')

    if not username or role != 'student':
        flash("Access denied! Please log in as a student.", "danger")
        return redirect(url_for('login'))
    messages = get_student_messages(username)
    marks=get_stud_mark(username)
    percent=get_percent(username)
    conn = get_db_connection()
    cursor = conn.cursor()
    # Query attendance counts
    cursor.execute("""
    SELECT status, COUNT(*) AS count
    FROM day_attendance
    WHERE username = %s
    GROUP BY status
""", (username,))
    results = cursor.fetchall()
    conn.close()

    # Convert to dictionary with default 0
    attendance = {'Present': 0, 'Absent': 0, 'Leave': 0}
    for row in results:
        attendance[row['status']] = row['count']
    conn=get_pay_db()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM payments WHERE stud_id=%s",(user_id,))
    pay=cursor.fetchone()
    conn.close()
    if pay:
        paid='paid'
    else:
        paid='not paid'
    

    return render_template(
        "student_dashboard.html",
        username=username,
        attendance=attendance,
        messages=messages,
        marks=marks,
        percent=percent,
        pay=paid

    )





    
