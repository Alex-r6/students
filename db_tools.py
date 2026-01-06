import sqlite3

db = './instance/students.sqlite3'

def get_students():
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''
    SELECT *
    FROM Студенты;
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return list(map(dict, data))

def show_best_students():
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''
    SELECT DISTINCT Студенты.фамилия, Журнал.оценка
    FROM Студенты
    INNER Join Журнал
    WHERE Студенты.id = Журнал.id_студента
    ORDER By Журнал.оценка DESC
    LIMIT 5;
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return list(map(dict,data))


def get_student(pk):
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''
    SELECT *
    FROM Студенты
    WHERE Студенты.id = ?;
    '''
    cursor.execute(query, [pk])
    data = cursor.fetchone()
    connection.close()
    return dict(data)

def get_groups():
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''
    SELECT *
    FROM Группы;
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return list(map(dict,data))


def show_facalty(pk):
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''
    SELECT  Факультеты.факультет
    FROM Факультеты
    JOIN Группы ON Группы.id_факульт = Факультеты.id
    JOIN Студенты ON Студенты.id_группы = Группы.id
    WHERE Студенты.id = ?;
    '''
    cursor.execute(query, [pk])
    data = cursor.fetchall()
    cursor.close()
    return list(map(dict,data))


def show_max_score():
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = '''
    SELECT Студенты.фамилия, Предметы.предмет, Журнал.оценка
    FROM Журнал
    JOIN Студенты ON Журнал.id_студента = Студенты.id
    JOIN Предметы ON Журнал.id_предмета = Предметы.id;
    '''
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return list(map(dict,data))
