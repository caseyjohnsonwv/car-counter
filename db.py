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

def fetch():
    conn,db = _connect()
    query="""
    SELECT * FROM dataLog WHERE id={}
    """.format(0)
    db.execute(query)
    res = db.fetchone()
    _quit(conn)
    return res

def generate():
    conn,db = _connect()
    query="""
    CREATE TABLE dataLog (
        id INTEGER NOT NULL PRIMARY KEY,
        carCount INTEGER,
        lastUpdate VARCHAR(50)
    )
    """
    try:
        db.execute(query)
    except Exception as ex:
        print("Failed to create dataLog table.")
        return
    _save(conn)
    _quit(conn)
    conn,db = _connect()
    query = """
    INSERT INTO dataLog VALUES (0, 0, NULL)
    """
    try:
        db.execute(query)
    except Exception as ex:
        print("Failed to insert first row into dataLog table.")
        return
    _save(conn)
    _quit(conn)

def reset():
    conn,db = _connect()
    query = """
    UPDATE dataLog SET carCount=0, lastUpdate=NULL WHERE id={}
    """.format(0)
    db.execute(query)
    _save(conn)
    _quit(conn)

def update(addition):
    data = fetch()
    conn,db = _connect()
    try:
        carCount = int(data[1])
    except Exception as ex:
        print(ex)
        carCount = 0
    carCount += addition
    timeNow = time.strftime("%H:%M:%S - %Y-%m-%d",time.gmtime())
    query = """
    UPDATE dataLog SET carCount={}, lastUpdate='{}' WHERE id={}
    """.format(carCount, timeNow, 0)
    db.execute(query)
    _save(conn)
    _quit(conn)

def view():
    conn,db = _connect()
    query = """
    SELECT * FROM dataLog
    """
    db.execute(query)
    res = db.fetchall()
    return res
