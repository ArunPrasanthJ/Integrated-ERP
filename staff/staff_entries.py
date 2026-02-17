from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from db import connect_test1, connect_payments

staff_entries = Blueprint('staff_entries', __name__, template_folder='../templates')

# helpers duplicated from staff_dashboard (to avoid circular import)
def get_stud(role):
    conn = connect_test1()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE role=%s", (role,))
    student_c = cursor.fetchall()
    cursor.close()
    conn.close()
    return student_c

def get_stud_paid():
    conn = connect_payments()
    cursor = conn.cursor()
    cursor.execute("SELECT stud_id FROM payments order by stud_id desc limit 1")
    student_p = cursor.fetchone()
    cursor.close()
    conn.close()
    return student_p


# --- Attendance entry page ---
@staff_entries.route('/staff/attendance_entry', methods=['GET', 'POST'])
def attendance_entry():
    if 'username' not in session or session.get('role') != 'staff':
        flash('Access denied! Please log in as staff.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
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
            flash('Attendance record added successfully.', 'success')
            return redirect(url_for('staff_entries.attendance_entry'))

    # fetch records for view
    conn = connect_test1()
    cursor = conn.cursor()
    cursor.execute("SELECT username, date, status FROM day_attendance ORDER BY date DESC")
    records = cursor.fetchall()
    cursor.close()
    conn.close()

    student_c = get_stud('student')
    count = len(student_c)
    student_p = get_stud_paid()
    c = len(student_p) if student_p else 0

    return render_template(
        'staff/attendance_entry.html',
        records=records,
        count=count,
        c=c,
        student_c=student_c,
        active='att_entry'
    )


# --- Marks entry page (subject-wise) ---
@staff_entries.route('/staff/marks_entry', methods=['GET', 'POST'])
def marks_entry():
    if 'username' not in session or session.get('role') != 'staff':
        flash('Access denied! Please log in as staff.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form.get('username')
        subject = request.form.get('subject')
        mark = request.form.get('mark')
        if username and subject and mark:
            # ensure the subject column exists in ca1
            conn = connect_test1()
            cursor = conn.cursor()
            try:
                cursor.execute(f"ALTER TABLE ca1 ADD COLUMN IF NOT EXISTS `{subject}` INT")
            except Exception:
                # some MySQL versions don't support IF NOT EXISTS on ALTER; ignore errors
                pass
            # insert or update row for student
            cursor.execute("SELECT id FROM ca1 WHERE name=%s", (username,))
            existing = cursor.fetchone()
            if existing:
                cursor.execute(f"UPDATE ca1 SET `{subject}`=%s WHERE name=%s", (mark, username))
            else:
                # build column list and values dynamically
                cursor.execute(f"INSERT INTO ca1 (name, `{subject}`) VALUES (%s, %s)", (username, mark))
            conn.commit()
            conn.close()
            flash('Mark recorded successfully.', 'success')
            return redirect(url_for('staff_entries.marks_entry'))

    # fetch current marks table
    conn = connect_test1()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ca1 ORDER BY name ASC")
    results = cursor.fetchall()
    # capture column names for display
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    student_c = get_stud('student')
    count = len(student_c)
    student_p = get_stud_paid()
    c = len(student_p) if student_p else 0

    return render_template(
        'staff/marks_entry.html',
        results=results,
        columns=columns,
        count=count,
        c=c,
        student_c=student_c,
        active='marks_entry'
    )
