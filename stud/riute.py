from flask import Flask, render_template,Blueprint

route = Blueprint('stud_route', __name__, template_folder='../templates')

@route.route('/feedback')
def feedback():
    return render_template('feedback.html')

@route.route('/exams')
def exams():
    return render_template('exam schedule.html')

@route.route('/lib')
def lib():
    return render_template('library.html')
