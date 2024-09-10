import sqlite3
from sqlite3 import Cursor

import a


def initiate_db():
    connection = sqlite3.Connection('Products.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)''')

    for i in range(1, 5):
        cursor.execute("INSERT OR IGNORE INTO Products(id, title, description, price) VALUES(?,?,?,?)",
                       (i, f'Название: Продукт{i}', f'Описание: Описание{i}', f'Цена {i * 100}'))

    connection.commit()
    connection.close()

    connect = sqlite3.Connection('Users.db')
    cur = connect.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL)''')




def add_user(username, email, age):
    initiate_db()
    connect = sqlite3.Connection('Users.db')
    cur = connect.cursor()
    cur.execute("INSERT INTO Users(username, email, age, balance) VALUES(?,?,?,?)",
                (username, email, age, '1000'))
    connect.commit()
    connect.close()


def is_included(username):
    initiate_db()
    connect = sqlite3.Connection('Users.db')
    cur = connect.cursor()
    cur.execute('''SELECT username FROM Users WHERE username=?''', (f'{username}',))
    if cur.fetchone() is None:
        return False
    else:
        return True

    connect.commit()
    connect.close()

def get_all_produkts():
    initiate_db()
    connection = sqlite3.Connection('Products.db')
    cursor = connection.cursor()
    y = [0]
    cursor.execute("SELECT title, description, price FROM Products")

    for i in cursor.fetchall():
        y.append(f' {i[0]} | {i[1]} | {i[2]}')
    return y

    connection.commit()
    connection.close()

