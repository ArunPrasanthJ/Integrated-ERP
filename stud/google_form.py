from flask import Flask, render_template, request, redirect, url_for, flash,Blueprint
from db import connect_details

student_f = Blueprint('stud_form', __name__, template_folder='../templates')

# DB connection helper
def get_db_connection():
    return connect_details()

# Display all Google Forms
@student_f.route("/index")
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id,form_name,form_id FROM google_forms ORDER BY id DESC")
    forms = cursor.fetchall()
    conn.close()
    return render_template("form.html", forms=forms)
