from flask import Flask, render_template, request, redirect, url_for,Blueprint
from db import connect_test1

admin_u = Blueprint('ad_u', __name__, template_folder='../templates')

@admin_u.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', '').strip()

        if username and password and role:
            conn = connect_test1()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, password, role)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('ad_u.manage_users'))

    # Fetch all users
    conn = connect_test1()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users ORDER BY id ASC")
    users = cursor.fetchall()
    conn.close()

    return render_template('addusers.html', users=users)

