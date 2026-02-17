from flask import Flask, render_template, request, redirect, url_for,Blueprint
from db import connect_test1, connect_payments, connect_details

admin_d = Blueprint('ad_d', __name__, template_folder='../templates')
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


# --- helper routes for manual data entry from admin dashboard ---
@admin_d.route('/add_attendance', methods=['POST'])
def add_attendance():
    username = request.form.get('username')
    date = request.form.get('date')
    status = request.form.get('status')
    if username and date and status:
        conn = connect_test1()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO day_attendance (username, date, status) VALUES (%s,%s,%s)",
            (username, date, status)
        )
        conn.commit()
        conn.close()
    return redirect(url_for('ad_d.admin_dashboard'))


@admin_d.route('/add_marks', methods=['POST'])
def add_marks():
    username = request.form.get('username')
    mark = request.form.get('mark')
    if username and mark:
        conn = connect_test1()
        cursor = conn.cursor()
        # ensure there is a mark column (MySQL 8+ supports IF NOT EXISTS)
        try:
            cursor.execute("ALTER TABLE ca1 ADD COLUMN IF NOT EXISTS mark VARCHAR(255)")
        except Exception:
            pass
        cursor.execute(
            "INSERT INTO ca1 (name, mark) VALUES (%s, %s)",
            (username, mark)
        )
        conn.commit()
        conn.close()
    return redirect(url_for('ad_d.admin_dashboard'))

@admin_d.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    student_username = request.form.get('student_username', '')  # selected student
    sender = 'admin'

    # Handle message sending
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

    # Fetch chat history for the selected student
    messages = []
    if student_username:
        conn = connect_test1()
        cursor = conn.cursor()  # use dictionary for easy access
        cursor.execute(
            "SELECT id, sender, message, created_at FROM query_messages WHERE student_username=%s ORDER BY created_at ASC",
            (student_username,)
        )
        messages = cursor.fetchall()
        conn.close()

    # Student list for dropdown
    role = 'student'
    student_c = get_stud(role)  
    count = len(student_c)

    # Paid students count
    student_p = get_stud_paid()
    c = len(student_p)
    #count forms
    conn = connect_details()
    cursor = conn.cursor()
    cursor.execute("SELECT form_name from google_forms")
    sheet_c = cursor.fetchall()
    cursor.close()
    sheet_count=len(sheet_c)

    return render_template(
        'a_dash.html',
        student_username=student_username,
        messages=messages,
        student_c=student_c,
        count=count,
        c=c,
        sheet_count=sheet_count
    )