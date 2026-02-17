from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from db import connect_test1,connect_payments,connect_details

staff_bp = Blueprint('staff_bp', __name__, template_folder='../templates')

# -----------------------------
# (use connection helpers directly)
# -----------------------------

def get_stud(role):
    conn = connect_test1()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE role=%s", (role,))
    student_c = cursor.fetchall()
    cursor.close()
    return student_c

def get_stud_paid():
    conn = connect_payments()
    cursor = conn.cursor()
    cursor.execute("SELECT stud_id FROM payments order by stud_id desc limit 1")
    student_p = cursor.fetchone()
    cursor.close()
    return student_p

# --- Main Staff Dashboard with Messages & Chart ---
@staff_bp.route('/staff_dashboard', methods=['GET', 'POST'])
def staff_main_dashboard():
    if 'username' not in session or session.get('role') != 'staff':
        flash('Access denied! Please log in as staff.', 'danger')
        return redirect(url_for('login'))
    
    student_username = request.form.get('student_username', '')
    sender = 'staff'

    if request.method == 'POST' and 'message' in request.form:
        message = request.form['message']
        if student_username and message.strip():
            conn = connect_test1()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO query_messages (sender, student_username, message) VALUES (%s, %s, %s)',
                (sender, student_username, message)
            )
            conn.commit()
            conn.close()

    messages = []
    if student_username:
        conn = connect_test1()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, sender, message, created_at FROM query_messages WHERE student_username=%s ORDER BY created_at ASC",
            (student_username,)
        )
        messages = cursor.fetchall()
        conn.close()

    role = 'student'
    student_c = get_stud(role)  
    count = len(student_c)
    student_p = get_stud_paid()
    c = len(student_p) if student_p else 0
    
    return render_template(
        'staff/staff_base.html',
        student_username=student_username,
        messages=messages,
        student_c=student_c,
        count=count,
        c=c,
        active='dashboard'
    )

# -----------------------------
# Staff attendance: show all students' day attendance
# -----------------------------
@staff_bp.route('/staff_attendance')
def staff_attendance():
    if 'username' not in session or session.get('role') != 'staff':
        flash('Access denied! Please log in as staff.', 'danger')
        return redirect(url_for('login'))

    conn = connect_test1()
    cursor = conn.cursor()
    cursor.execute("SELECT username, date, status FROM day_attendance ORDER BY date DESC")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Get count and paid count for base template
    student_c = get_stud('student')
    count = len(student_c)
    student_p = get_stud_paid()
    c = len(student_p) if student_p else 0
    
    return render_template('staff/staff_attendance.html', records=records, count=count, c=c, student_c=student_c, active='attendance')


# -----------------------------
# Staff results: list marks for all students
# -----------------------------
@staff_bp.route('/staff_results')
def staff_results():
    if 'username' not in session or session.get('role') != 'staff':
        flash('Access denied! Please log in as staff.', 'danger')
        return redirect(url_for('login'))

    conn = connect_test1()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ca1 ORDER BY name ASC")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Get count and paid count for base template
    student_c = get_stud('student')
    count = len(student_c)
    student_p = get_stud_paid()
    c = len(student_p) if student_p else 0
    
    return render_template('staff/staff_results.html', results=results, count=count, c=c, student_c=student_c, active='results')
