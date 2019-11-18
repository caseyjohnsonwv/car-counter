import psycopg2 as DBLIB
import os, time


def _connect():
    conn = DBLIB.connect(os.environ['DATABASE_URL'])
    db = conn.cursor()
    return conn,db

def _save(conn):
    conn.commit()

def _quit(conn):
    conn.close()

def drop_all():
    conn,db = _connect()
    query = """
    DROP TABLE today
    """
    try:
        db.execute(query)
    except Exception as ex:
        print(ex)
    query = """
    DROP TABLE history
    """
    try:
        db.execute(query)
    except Exception as ex:
        print(ex)
    _save(conn)
    _quit(conn)

def fetchToday():
    conn,db = _connect()
    query = """
    SELECT carCount, lastUpdate FROM today
    """
    db.execute(query)
    res = db.fetchall()
    _quit(conn)
    return res

def fetchHistory():
    conn,db = _connect()
    query = """
    SELECT totalCount, lastUpdate FROM history
    """
    db.execute(query)
    res = db.fetchall()
    _quit(conn)
    return res

def generate():
    #create tables
    conn,db = _connect()
    query="""
    CREATE TABLE today (
        id INTEGER NOT NULL PRIMARY KEY,
        carCount INTEGER,
        lastUpdate VARCHAR(50)
    )
    """
    try:
        db.execute(query)
        _save(conn)
    except Exception as ex:
        print("Failed to create today table.")
    query = """
    CREATE TABLE history (
        id INTEGER NOT NULL PRIMARY KEY,
        totalCount INTEGER,
        lastUpdate VARCHAR(50)
    )
    """
    try:
        db.execute(query)
        _save(conn)
    except Exception as ex:
        print("Failed to create history table.")
    _quit(conn)

def resetToday():
    conn,db = _connect()
    query = """
    DELETE FROM today
    """
    db.execute(query)
    _save(conn)
    _quit(conn)

def resetHistory():
    conn,db = _connect()
    query = """
    DELETE FROM history
    """
    db.execute(query)
    _save(conn)
    _quit(conn)

def updateToday(carCount):
    conn,db = _connect()
    query = """
    SELECT id FROM today
    """
    db.execute(query)
    nextId = len(db.fetchall())
    timeNow = time.strftime("%H:%M:%S - %Y-%m-%d",time.gmtime())
    query = """
    INSERT INTO today VALUES ({}, {}, '{}')
    """.format(nextId, carCount, timeNow)
    db.execute(query)
    _save(conn)
    _quit(conn)

def updateHistory():
    query = """
    SELECT carCount, lastUpdate FROM today
    """
    conn,db = _connect()
    db.execute(query)
    totalCount = 0
    lastUpdate = None
    res = db.fetchall()
    for row in res:
        carCount = row[0]
        totalCount += int(carCount)
    lastUpdate = res[-1][1]
    query = """
    SELECT totalCount, lastUpdate FROM history
    """
    db.execute(query)
    res = db.fetchall()
    query = """
    DELETE FROM history *
    """
    db.execute(query)
    query = "INSERT INTO history VALUES (0, {}, '{}'),".format(totalCount, lastUpdate)
    for k in range(len(res)):
        ct = res[k][0]
        up = res[k][1]
        query += "({},{},'{}'),".format(k+1, ct, up)
    query = query[:-1]
    db.execute(query)
    _save(conn)
    _quit(conn)

def viewToday():
    conn,db = _connect()
    query = """
    SELECT * FROM today
    """
    db.execute(query)
    res = db.fetchall()
    return res

def viewHistory():
    conn,db = _connect()
    query = """
    SELECT * FROM history
    """
    db.execute(query)
    res = db.fetchall()
    return res
