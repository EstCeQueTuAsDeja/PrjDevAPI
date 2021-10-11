0# -*- coding: utf-8 -*-
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

def addDevice(deviceName, model, location, serial, snmpcomm, conn):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO devices(name, model, location, serial, comSNMP) VALUES(?,?,?,?,?)""", (deviceName, model, location, serial, snmpcomm))
    conn.commit()
    
def removeDeviceByName(deviceName, conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT id FROM devices WHERE name='"""+deviceName+"""'""")
    allDeviceID = cursor.fetchall()
    for deviceID in allDeviceID:
        cursor.execute("""DELETE FROM devices WHERE id ="""+str(deviceID[0]))
        conn.commit()

def removeDeviceById(idDevice, conn):
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM devices WHERE id ="""+str(idDevice))
    conn.commit()

def selectDeviceByName(deviceName, conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM devices WHERE name='"""+str(deviceName))
    device = cursor.fetchall()
    return device

def selectAll(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM devices""")
    allDevice = cursor.fetchall()
    return allDevice

def selectAllOids(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM oids""")
    allOids = cursor.fetchall()
    return allOids

def addOids(oidName, oid, conn):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO oids(name, oid) VALUES(?,?)""", (oidName, oid))
    conn.commit()

def removeOidsById(idOid, conn):
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM devices WHERE id ="""+str(idOid))
    conn.commit()
    
def selectAllRequ(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM poller""")
    allRequ = cursor.fetchall()
    return allRequ

def addRequ(idDevices, idOid, timer, conn):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO poller(idDevices,idOids,timer) VALUES(?,?,?)""", (idDevices, idOid, timer))
    conn.commit()

def removeRequById(idRequ, conn):
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM poller WHERE id ="""+str(idRequ))
    conn.commit()

def removeRequByIdDevices(idDevices, conn):
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM poller WHERE idDevices ="""+str(idDevices))
    conn.commit()
    
def removeRequByidOid(idOid, conn):
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM poller WHERE idOid ="""+str(idOid))
    conn.commit()

def selectAllLog(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM logs""")
    allLog = cursor.fetchall()
    return allLog

def addLog(idDevices, log, conn):
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO logs(idDevices,log) VALUES(?,?)""", (idDevices, log))
    conn.commit()
    
def removeAllLog(idRequ, conn):
    cursor = conn.cursor()
    cursor.execute("""DELETE FROM logs""")
    conn.commit()

def countError(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT COUNT(*) FROM logs""")
    countLog = cursor.fetchall()
    return countLog[0][0]

def countErrorFromTenDay(conn):
    cursor = conn.cursor()
    cursor.execute("""SELECT DATE(timestamp) AS Date, COUNT(*) AS id 
                           FROM logs 
                           WHERE 
                               timestamp >= (DATE() - '10 day') 
                           GROUP BY 
                               DATE(timestamp)""")
    countLog = cursor.fetchall()
    return countLog[0]

def countErrorFromGivenDay(numday,conn):
    cursor = conn.cursor()
    stattab = []
    for i in range(0,numday+1):
        cursor.execute("""SELECT COUNT(*) FROM logs WHERE DATE(timestamp) == DATE(timestamp,'-"""+str(i)+""" day')""")
                               
        countLog = cursor.fetchall()
        stattab.append(countLog[0][0])
    return stattab

conn = connect()
initdB.end(conn)