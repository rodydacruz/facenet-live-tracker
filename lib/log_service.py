import sqlite3
import datetime

class LogRepository:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS last_seen (
                person_id INTEGER,
                location TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(person_id) REFERENCES person(id)
            )
        ''')
        self.conn.commit()

    def log_last_seen(self, person_id, location):
        # Check if there's already a log entry for this person at this location
        self.cursor.execute('''
            SELECT COUNT(*) FROM last_seen WHERE person_id=? AND location=?
        ''', (person_id, location))
        count = self.cursor.fetchone()[0]
        if count > 0:
            # Update the timestamp
            current_time = datetime.datetime.now()
            self.cursor.execute('''
                UPDATE last_seen SET timestamp=? WHERE person_id=? AND location=?
            ''', (current_time, person_id, location))
        else:
            # Insert a new log entry
            self.cursor.execute('''
                INSERT INTO last_seen (person_id, location)
                VALUES (?, ?)
            ''', (person_id, location))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_last_seen(self, person_id):
        self.cursor.execute('''
            SELECT location, timestamp FROM last_seen WHERE person_id=?
            ORDER BY timestamp DESC LIMIT 1
        ''', (person_id,))
        return self.cursor.fetchone()

    def __del__(self):
        self.conn.close()