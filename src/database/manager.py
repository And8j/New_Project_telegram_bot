import sqlite3
from queue import Queue
from threading import Lock
from pathlib import Path
from contextlib import contextmanager


class DatabaseManager:
    def __init__(self, db_path: str = "data/database.db", pool_size: int = 10):
        self.db_path = db_path
        self.pool_size = pool_size
        self.pool = Queue(maxsize=pool_size)
        self.lock = Lock()

        # I first create a connection pool.
        for _ in range(pool_size):
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            self.pool.put(conn)

    def init_database(self, schema_path: str = "src/database/schema.sql"):
        """
        I initialize the database by creating tables from schema.sql.
        """
        schema_file = Path(schema_path)
        if not schema_file.exists():
            raise FileNotFoundError(f"❌ Schema file not found: {schema_path}")

        with open(schema_file, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        with self.connection() as conn:
            conn.executescript(schema_sql)
            conn.commit()

    @contextmanager
    def connection(self):
        """
        Context manager for getting a connection from the pool.
        """
        conn = self.pool.get()
        try:
            yield conn
        finally:
            self.pool.put(conn)

    def execute_query(self, query: str, params: tuple = ()):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid

    def fetch_one(self, query: str, params: tuple = ()):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

    def fetch_all(self, query: str, params: tuple = ()):
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def close_all_connections(self):
        """
        Close all connections before the program ends.
        """
        with self.lock:
            while not self.pool.empty():
                conn = self.pool.get()
                conn.close()
