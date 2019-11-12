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
    DROP TABLE dataLog
    """
    db.execute(query)
    _save(conn)
    _quit(conn)

def fetch(id):
    conn,db = _connect()
    query="""
    SELECT * FROM dataLog WHERE id={}
    """.format(id)
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
        totalCount INTEGER,
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
    INSERT INTO dataLog VALUES (0, 0, 0, NULL)
    """
    try:
        db.execute(query)
    except Exception as ex:
        print("Failed to insert first rows into dataLog table.")
        return
    _save(conn)
    _quit(conn)

def reset(id):
    conn,db = _connect()
    query = """
    UPDATE dataLog SET carCount=0, totalCount=0, lastUpdate=NULL WHERE id={}
    """.format(id)
    db.execute(query)
    _save(conn)
    _quit(conn)

def update(carCount, id):
    data = fetch(0)
    conn,db = _connect()

    #update id=0, total reading
    try:
        totalCount = int(data[2])
    except Exception as ex:
        print(ex)
        totalCount = 0
    totalCount += carCount
    timeNow = time.strftime("%H:%M:%S - %Y-%m-%d",time.gmtime())
    query = """
    UPDATE dataLog SET carCount={}, totalCount={}, lastUpdate='{}' WHERE id={}
    """.format(carCount, totalCount, timeNow, id)
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
