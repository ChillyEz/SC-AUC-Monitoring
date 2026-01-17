import os
import sqlite3


class ItemsDatabase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)")
        self.connection.commit()

    def insert_item(self, name):
        self.cursor.execute("INSERT INTO items (name) VALUES (?)", (name,))
        self.connection.commit()

    def get_items(self):
        self.cursor.execute("SELECT * FROM items")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()