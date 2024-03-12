import sqlite3

class PersonRepository:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS person (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                email TEXT,
                photo_url TEXT
            )
        ''')
        self.conn.commit()

    def create_person(self, name, age, email=None, photo_url=None):
        self.cursor.execute('''
            INSERT INTO person (name, age, email, photo_url)
            VALUES (?, ?, ?, ?)
        ''', (name, age, email, photo_url))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_person(self, person_id):
        self.cursor.execute('''
            SELECT * FROM person WHERE id=?
        ''', (person_id,))
        return self.cursor.fetchone()

    def update_person(self, person_id, name=None, age=None, email=None, photo_url=None):
        update_values = {}
        if name is not None:
            update_values['name'] = name
        if age is not None:
            update_values['age'] = age
        if email is not None:
            update_values['email'] = email
        if photo_url is not None:
            update_values['photo_url'] = photo_url

        update_query = 'UPDATE person SET '
        update_query += ', '.join([f'{key}=?' for key in update_values.keys()])
        update_query += ' WHERE id=?'

        values = list(update_values.values())
        values.append(person_id)

        self.cursor.execute(update_query, tuple(values))
        self.conn.commit()

    def delete_person(self, person_id):
        self.cursor.execute('''
            DELETE FROM person WHERE id=?
        ''', (person_id,))
        self.conn.commit()

    def get_all_persons(self):
        self.cursor.execute('''
            SELECT * FROM person
        ''')
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()
