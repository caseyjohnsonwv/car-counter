import psycopg2 as DBLIB
import os, time


class db:
    def __init__(self):
        self.conn = None
        self.db = None

    def _connect(self):
        self.conn = DBLIB.connect(os.environ['db_url'])
        self.db = conn.cursor()

    def _save(self):
        self.conn.commit()
        self.conn.close()
        self.conn = None
        self.db = None

    def _generate(self):
        self._connect()
        query="""
        CREATE TABLE dataLog (
            id INTEGER NOT NULL PRIMARY KEY,
            carCount INTEGER,
            lastUpdate VARCHAR(50),
        )
        """
        self.execute(query)
        self._save()

    def execute(self, query):
        self._connect()
        self.db.execute(query)
        self._save()

    def fetch(self):
        self._connect()
        query = """
        SELECT * FROM dataLog
        """
        self.execute(query)
        res = self.db.fetchone()
        self._save()
        return res

    def log(self, carCount):
        timeNow = time.strftime("%H:%M:%S - %Y-%m-%d",time.gmtime())
        query="""
        UPDATE dataLog SET carCount={}, lastUpdate={} WHERE id={}
        """.format(carCount, timeNow, 0)
        self.execute(query)
