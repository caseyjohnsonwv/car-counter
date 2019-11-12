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
    db.execute(query)
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

def generate():
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
    except Exception as ex:
        print("Failed to create today table.")
        return
    _save(conn)
    _quit(conn)
    conn,db = _connect()
    query = """
    INSERT INTO today VALUES (0, 0, NULL)
    """
    try:
        db.execute(query)
    except Exception as ex:
        print("Failed to insert first rows into today table.")
        return
    _save(conn)
    _quit(conn)

def resetToday():
    conn,db = _connect()
    query = """
    UPDATE today SET totalCount=0, lastUpdate=NULL WHERE id=0
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
    totalCount += carCount
    timeNow = time.strftime("%H:%M:%S - %Y-%m-%d",time.gmtime())
    query = """
    UPDATE today SET totalCount={}, lastUpdate='{}' WHERE id={}
    """.format(totalCount, timeNow, id)
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
