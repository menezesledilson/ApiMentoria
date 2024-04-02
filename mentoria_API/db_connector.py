import sqlite3

class DBConnector:
    def __init__(self,db_path) :
        self.db_patch = db_path
    
    def connect(self):
        conn = sqlite3.connect(self.db_patch)
        return conn