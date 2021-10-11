# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 15:20:44 2021

@author: raffelet
"""

import sqlite3
from pathlib import Path

DATABASE = './datab/prjsnmp.db'
        
def init():
    conn = sqlite3.connect(DATABASE)
    return conn

def returnPath(DATABASE):
    return DATABASE
    
def end(conn):
    conn.close()

def dbCreate():
    conn = init()
    initDevices(conn)
    initOids(conn)
    initLogs(conn)
    initPoller(conn)
    return conn

def initDevices(conn):
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS devices(
                           id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                           name TEXT,
                           model TEXT,
                           location TEXT,
                           serial TEXT,
                           comSNMP TEXT
                           )
                   """)
    conn.commit()

def initOids(conn):
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS oids(
                           id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                           name TEXT,
                           oid TEXT
                           )
                   """)
    conn.commit()
    
def initLogs(conn):
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS logs(
                           id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                           idDevices INTEGER,
                           timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                           log TEXT,
                           FOREIGN KEY (idDevices) REFERENCES devices(id)
                           )
                   """)
    conn.commit()
    
def initPoller(conn):
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS poller(
                           id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                           idDevices INTEGER,
                           idOids INTEGER,
                           timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                           timer INTEGER,
                           FOREIGN KEY (idDevices) REFERENCES devices(id),
                           FOREIGN KEY (idOids) REFERENCES oids(id)
                           )
                   """)
    conn.commit()

