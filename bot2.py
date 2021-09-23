# https://surik00.gitbooks.io/aiogram-lessons/content/chapter1.html
# import sqlalchemy
# from sqlalchemy import create_engine
# engine = create_engine('sqlite:///:memory:', echo=True)
# print("Версия SQLAlchemy:", sqlalchemy.__version__)
#
# from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
# metadata = MetaData()
# users_table = Table('tasks', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('task_name', String),
#     Column('task_text', String),
#     Column('task_rating', String),
#     Column('task_category', String),
#     Column('task_status', String)
# )
# metadata.create_all(engine)
#
# class Task(object):
#     def __init__(self, task_name, task_text, task_rating, task_category, task_status):
#         self.task_name = task_name
#         self.task_text = task_text
#         self.task_rating = task_rating
#         self.task_category = task_category
#         self.task_status = task_status
#
#     def __repr__(self):
#         return "<Task('%s', '%s', '%s', '%s', '%s')>" % (self.task_name, self.task_text, self. task_rating, self.task_category, self.task_status)
#
#

# https://ru.wikibooks.org/wiki/SQLAlchemy
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import api_key
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
import random
import time



engine = create_engine('sqlite:///bot_database.db')
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

mapper(Task, tasks_table)

def add_task(name, description):
    task = Task(name, False, description)
    session.add(task)
    session.commit()
    print(("'")+str(name)+("'")+'-task is written to the database')






bot = Bot(token=api_key)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nНапиши мне что-нибудь!")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")

@dp.message_handler()
async def echo_message(msg: types.Message):
    if msg.text.lower() == 'список':
        text_task = 'Список:\n'
        for instance in session.query(Task).order_by(Task.id):
            text_task += '\n' + str(instance.id) + ' ' + instance.name + ' ' + str(instance.completed)
            print(instance.id, instance.name, instance.description)

        print(text_task)
        await bot.send_message(msg.from_user.id, text_task)

    elif msg.text.lower() == 'вопрос':
        text_task = 'Вопрос:\n'
        rand = random.randrange(0, session.query(Task).count())
        row = session.query(Task)[rand]
        print(row.name)


        # for instance in session.query(Task).order_by(Task.id):
        #     text_task += '\n' + str(instance.id) + ' ' + instance.name + ' ' + str(instance.completed)
        #     print(instance.id, instance.name, instance.description)

        print(text_task)
        await bot.send_message(msg.from_user.id, row.name)
        time.sleep(20)
        await bot.send_message(msg.from_user.id, row.description)

    elif msg.text.lower().split(' ')[0] == 'уд':
        del_id = msg.text.lower().split(' ')[1]
        print(del_id)
        del_query = session.query(Task).filter(Task.id == int(del_id))
        instance_text = ''
        for instance in del_query:
            instance_text += str(instance.name)
            print(instance)
            print(instance.name)
        print(del_query)
        del_query.delete()
        # del_query.commit()
        await bot.send_message(msg.from_user.id, "Удаление задачи из базы:" + instance_text)
    elif msg.text.lower().split(' ')[0] == 'вып':
        complete_id = msg.text.lower().split(' ')[1]
        print(complete_id)
        complete_query = session.query(Task).filter(Task.id == int(complete_id))
        for instance in complete_query:
            print(instance)
        complete_query.update({Task.completed: 1})
        session.commit()
        complete_text = ''
        for instance in complete_query:
            print(instance)
            complete_text +=  str(instance)
        await bot.send_message(msg.from_user.id, "Задача выполнена: " + complete_text)

    else:
        try:
            task_name = str(msg.text).split('/')[0]
            task_description = str(msg.text).split('/')[1]
            add_task(task_name, task_description)
            await bot.send_message(msg.from_user.id, "Вопрос добавлен: " + task_name)
        except Exception as e:
            print(e)
            await bot.send_message(msg.from_user.id, "1. Напиши Вопрос/ответ чтобы добавить в базу\n2. Напиши слово список чтбы получить список задач\n3. Если задача выполнена напиши вып 3\n4. Чтобы удалить из базы задачу напиши уд 2")



executor.start_polling(dp)