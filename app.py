from flask import Flask, render_template, request, url_for, redirect
from db_tools import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', students_list=get_students(), best_students=show_best_students(),
                           groups=get_groups(), show_max_score=show_max_score())


@app.route('/student/<int:pk>/')
def student_detail(pk):
    student = get_student(pk)
    faculties = show_facalty(pk)
    return render_template('student_detail.html', student=student, faculties=faculties)


if __name__ == '__main__':
    app.run(debug=True)