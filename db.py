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
    query="""
    SELECT * FROM today WHERE id=0
    """
    db.execute(query)
    res = db.fetchone()
    _quit(conn)
    return res

def fetchHistory():
    conn,db = _connect()
    query = """
    SELECT * FROM history
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
        totalCount INTEGER,
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
        totalCount INTEGER
    )
    """
    try:
        db.execute(query)
        _save(conn)
    except Exception as ex:
        print("Failed to create history table.")
    _save(conn)
    #upload initial data
    conn,db = _connect()
    query = """
    INSERT INTO today VALUES (0, 0, NULL)
    """
    try:
        db.execute(query)
        _save(conn)
    except Exception as ex:
        print("Failed to insert first row into today table.")
    query = "INSERT INTO history VALUES "
    for k in range(14):
        query += "({},0),".format(k)
    query = query[:-1]
    try:
        db.execute(query)
        _save(conn)
    except Exception as ex:
        print("Failed to insert dummy rows into history table.")
    _quit(conn)

def resetToday():
    conn,db = _connect()
    query = """
    UPDATE today SET totalCount=0, lastUpdate=NULL WHERE id=0
    """
    db.execute(query)
    _save(conn)
    _quit(conn)

def resetHistory():
    conn,db = _connect()
    query = """
    UPDATE history SET totalCount=0
    """
    db.execute(query)
    _save(conn)
    _quit(conn)

def updateToday(carCount):
    data = fetchToday()
    conn,db = _connect()
    try:
        id, totalCount, lastUpdate = data
        totalCount = int(totalCount)
    except Exception as ex:
        print(ex)
        totalCount = 0
    timeNow = time.strftime("%H:%M:%S - %Y-%m-%d",time.gmtime())
    totalCount += carCount
    query = """
    UPDATE today SET totalCount={}, lastUpdate='{}' WHERE id={}
    """.format(totalCount, timeNow, id)
    db.execute(query)
    _save(conn)
    _quit(conn)

def updateHistory():
    data = fetchToday()
    conn,db = _connect()
    try:
        id, totalCount, lastUpdate = data
        totalCount = int(totalCount)
    except Exception as ex:
        print(ex)
        totalCount = 0
    query = """
    SELECT * FROM history
    """
    db.execute(query)
    res = db.fetchall()
    query = """
    DELETE FROM history *
    """
    db.execute(query)
    query = "INSERT INTO history VALUES (0, {}),".format(totalCount)
    for k in range(0,13):
        ct = res[k][1]
        query += "({},{}),".format(k+1,ct)
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
    res = db.fetchone()
    return res

def viewHistory():
    conn,db = _connect()
    query = """
    SELECT * FROM history
    """
    db.execute(query)
    res = db.fetchall()
    return res
