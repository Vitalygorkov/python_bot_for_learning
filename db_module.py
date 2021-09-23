# https://docs.sqlalchemy.org/en/14/core/engines.html
# https://ru.wikibooks.org/wiki/SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker

engine = create_engine('sqlite:///mydatabase.db')
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.types import Boolean
metadata = MetaData()
tasks_table = Table('tasks', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('completed', Boolean),
    Column('description', String)
                    )
metadata.create_all(engine)


class Task(object):
    def __init__(self, name, completed, description):
        self.name = name
        self.completed = completed
        self.description = description

    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.name, self.completed, self.description)

metadata.create_all(engine)
mapper(Task, tasks_table)
# print(mapper(Task, tasks_table))

# task1 = Task('make a bot for processing tasks', 'master the use of orm databases, write command handlers and bot logic')
# session.add(task1)
# session.commit()

# ourTask = session.query(Task).first()

def add_task(name, completed, description):
    task = Task(name, completed, description)
    session.add(task)
    session.commit()
    print(("'")+str(name)+("'")+'-task is written to the database')

add_task('new task2', True, 'new task description2')

task_string = 'Это задача/это описание задачи'

task_name = task_string.split('/')[0]
task_description = task_string.split('/')[1]
print(task_name)
print(task_description)


# print(ourTask)
# print(task1)
# print(task1.id)
# text_task = ''
# for instance in session.query(Task).order_by(Task.id):
#     text_task += '\n' + str(instance.id) + ' ' + instance.name
#     print(instance.id, instance.name, instance.description)