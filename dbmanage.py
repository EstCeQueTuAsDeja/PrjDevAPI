# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 11:43:19 2021

@author: raffelet
"""
import sqlite3
import initdatabase as initdB
from pathlib import Path


def connect():
    my_file = Path(initdB.DATABASE)

    if my_file.is_file():
        conn = initdB.init()
    else:
        conn = initdB.dbCreate()
    return conn


def addDevice(model, autonomie, conn):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO voitures(model, autonomie) VALUES(?,?)""", (model, autonomie))
    conn.commit()
    

def selectAll(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM voitures""")
    allDevice = cursor.fetchall()
    return allDevice


conn = connect()
addDevice("testla","840",conn)




initdB.end(conn)