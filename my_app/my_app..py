from typing import List
import os

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
UPLOAD_FOLDER = './static/img/user_img/'

# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.sqlite3"
app.config["SECRET_KEY"] = "blabla_333"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)
# initialize the app with the extension
db.init_app(app)


class Worker(db.Model):
    __tablename__ = 'workers'
    id: Mapped[int] = mapped_column(primary_key=True,  autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    department_id: Mapped[int] = mapped_column(ForeignKey('departments.id'))

    department: Mapped['Department'] = relationship(back_populates='staff')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Department(db.Model):
    __tablename__ = 'departments'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    staff: Mapped[List[Worker]] = relationship(back_populates='department')


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str]
    img: Mapped[str]


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).where(User.id == user_id)).scalar()


@app.route('/')
def index():
    worker_list = db.session.execute(db.select(Worker)).scalars()
    dep_list = db.session.execute(db.select(Department)).scalars()
    return render_template('index.html', worker_list=worker_list, dep_list=dep_list)


@app.route('/add/worker', methods=['POST'])
def add_worker():
    username = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    dep_id = request.form.get('dep_id')
    new_worker = Worker(username=username, first_name=first_name, last_name=last_name, department_id=dep_id)
    db.session.add(new_worker)
    db.session.commit()
    return redirect(url_for('index'))


# with app.app_context():
#     db.create_all()
#
if __name__ == '__main__':
    app.run(debug=True)


    # d1 = Department(name='Developers')
    # d2 = Department(name='Sales')
    # d3 = Department(name='Management')
    # db.session.add_all([d1,d2,d3])
    # db.session.commit()

    # w1 = Worker(first_name='Alex', last_name='Popov', username='qaz', department_id=1)
    # w2 = Worker(first_name='Max', last_name='Pipiv', username='qazon', department_id=3)
    # w3 = Worker(first_name='Rex', last_name='Pipov', username='qazelle', department_id=2)
    # db.session.add_all([w1,w2,w3])
    # db.session.commit()