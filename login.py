from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_wtf import FlaskForm

# ensure databases/tables exist on startup
from db_setup import initialize_all
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from stud.attendance import student_bp
from stud.stud_dashboard import studentatt_bp
from stud.google_form import student_f
from stud.stud_marks import student_m

from stud.pay import student_p
from stud.allocate import student_al
from stud.riute import route
from admin.admin_dashboard import admin_d

# staff module
from staff.staff_dashboard import staff_bp
from staff.staff_entries import staff_entries
from admin.admin_adduser import admin_u
from admin.admin_paydetails import admin_p
from admin.admission_staff_sheets import admin_s
from admin.admin_table import admin_t

# --- JWT Imports ---
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

# --- ensure database schemas exist ---
initialize_all()

# --- App Setup ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'  # JWT secret
app.register_blueprint(student_bp)
app.register_blueprint(studentatt_bp)
app.register_blueprint(student_f)
app.register_blueprint(student_m)
app.register_blueprint(student_p)
app.register_blueprint(student_al)
app.register_blueprint(route)
app.register_blueprint(admin_d)
app.register_blueprint(admin_u)
app.register_blueprint(admin_p)
app.register_blueprint(admin_s)
app.register_blueprint(admin_t)
# register staff blueprint
app.register_blueprint(staff_bp)
app.register_blueprint(staff_entries)
app.permanent_session_lifetime = timedelta(minutes=30)

jwt = JWTManager(app)

# --- Database Connection ---
from db import connect_test1

# --- Forms ---
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# --- Authentication ---
def authenticate(username, password):
    conn = connect_test1()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username=%s AND password=%s"
            cursor.execute(sql, (username, password))
            return cursor.fetchone()
    finally:
        conn.close()

# --- Combined Auth Check ---
def is_authenticated(required_role=None):
    # --- Session check ---
    if 'username' in session:
        if required_role and session.get('role') != required_role:
            return False
        return True

    # --- JWT check ---
    try:
        identity = get_jwt_identity()
        if identity:
            if required_role and identity.get('role') != required_role:
                return False
            return True
    except Exception:
        return False

    return False

# --- Routes ---
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = authenticate(username, password)
        if user:
            role = user['role']

            # --- Store in Session ---
            session.permanent = True
            session['username'] = user['username']
            session['role'] = role
            session['id'] = user['id']

            # --- Create JWT Token ---
            access_token = create_access_token(identity={
                'username': user['username'],
                'role': role
            })


            # Redirect by role (browser flow)
            if role == 'student':
                return redirect(url_for('stud.student_dashboard'))
            elif role == 'staff':
                return redirect(url_for('staff_bp.staff_main_dashboard'))
            elif role == 'admin':
                return redirect(url_for('ad_d.admin_dashboard'))
            else:
                flash('Unknown role', 'danger')
                return redirect(url_for('login'))
        else:
            flash('User name or password is not correct', 'danger')
    return render_template('login.html', form=form)

# --- Logout ---
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for('login'))

# --- Dashboards ---
@app.route('/to_stud_dash')
@jwt_required(optional=True)
def to_stud_dash():
    if not is_authenticated('student'):
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))
    username = session.get('username') or get_jwt_identity()['username']
    return redirect(url_for('stud.student_dashboard'))

@app.route('/staff_dashboard')
@jwt_required(optional=True)
def staff_dashboard():
    # forward to blueprint route to maintain context
    if not is_authenticated('staff'):
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))
    return redirect(url_for('staff_bp.staff_main_dashboard'))

@app.route('/admin_dashboard')
@jwt_required(optional=True)
def admin_dashboard():
    if not is_authenticated('administrative_department'):
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))
    username = session.get('username') or get_jwt_identity()['username']
    return render_template('admin_dashboard.html', username=username)

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True)
