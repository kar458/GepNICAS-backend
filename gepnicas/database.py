import psycopg2
from psycopg2 import sql
import config

class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        if self.conn is None or self.conn.closed != 0:
            self.conn = psycopg2.connect(
                dbname=config.DB_NAME,
                user=config.DB_USER,
                password=config.DB_PASSWORD,
                host=config.DB_HOST,
                port=config.DB_PORT
            )

    def execute(self, query, params=None):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        cursor.close()

    def fetchall(self, query, params=None):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        records = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        return [dict(zip(columns, row)) for row in records]

    def fetchone(self, query, params=None):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        record = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        return dict(zip(columns, record)) if record else None

db = Database()
