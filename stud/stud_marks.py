from flask import Flask, render_template, request,Blueprint,session
from db import connect_test1

student_m = Blueprint('stud_mark', __name__, template_folder='../templates')



@student_m.route("/mark")
def mark():
    student_data = None
    user_name = session['username']
    conn = connect_test1()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ca1 WHERE name=%s", (user_name,))
    student_data = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("result.html", student=student_data)

