from flask import Flask, render_template, request
import psycopg2
from contextlib import closing
from psycopg2 import sql
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, String, MetaData, Integer
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
db_string = "postgres://postgres:admin@localhost:5432/hospital_med"
db = create_engine(db_string)
meta = MetaData(db)

drugs_table = Table('Inventory', meta,
                    Column('name', String),
                    Column('country', String))
actions_table = Table('actions',meta,
                      Column('id', Integer, primary_key=True),
                      Column('act_type',String))


# with db.connect() as conn:
# insert_statement = drugs_table.insert().values(name="Нурофен2", country="Україна")
# conn.execute(insert_statement)

# def Sql_get_data():
#     with closing(psycopg2.connect(dbname='hospital_med', user='postgres',
#                                   password='admin', host='localhost')) as conn:
#         with conn.cursor() as cursor:
#             conn.autocommit = True
#             cursor.execute('SELECT name FROM hospital LIMIT 20')
#             values = []
#             for row in cursor:
#                 values.append(row)
#             print(values)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('Login.html')


@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    items = []
    items_action = []
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        sql_add_data(name, country)
    items = get_data_database_drugs()
    items_action = get_data_unit()

    return render_template('add_data.html', items=items, items_action=items_action)


@app.route('/userpanel')
def user_panel():
    return render_template('userPanel.html')


def get_data_unit():
    items_action = []
    with closing(psycopg2.connect(dbname='hospital_med', user='postgres',
                                  password='admin', host='localhost')) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute('SELECT units_type FROM conditional'
                           '_units')
            for row in cursor:
                items_action.append(str(row)[2:-3])
                print(row)
    return items_action


def get_data_database_drugs ():
    items = []
    with closing(psycopg2.connect(dbname='hospital_med', user='postgres',
                                  password='admin', host='localhost')) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute('SELECT name FROM Inventory')
            for row in cursor:
                items.append(str(row)[2:-3])
    cursor.close()
    return items


def sql_add_data(name, country):
    with closing(psycopg2.connect(dbname='hospital_med', user='postgres',
                                  password='admin', host='localhost')) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            values = [(name, country), ]
            insert = sql.SQL('insert into Inventory (name,country) values {}').format(
                sql.SQL(',').join(map(sql.Literal, values)))
            cursor.execute(insert)
            cursor.execute('SELECT * FROM Inventory LIMIT 5')
            for row in cursor:
                print(row)


def sql_get_data():
    with closing(psycopg2.connect(dbname='hospital_med', user='postgres',
                                  password='admin', host='localhost')) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            items = cursor.execute('SELECT * FROM Inventory LIMIT 5')
            for row in cursor:
                print(row)
    return items


if __name__ == '__main__':
    app.run()
