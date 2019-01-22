import psycopg2
from .queries import tables


class DbModels:
    """contains the functions that pertain the database connection"""

    def db_connection(self):
        """this method creates the connection to the database and returns a conn object"""
        conn = psycopg2.connect("dbname = questioner user = postgres password = 0001")
        return conn
    

    def create_table(self, tables):
        """this creates all tables"""
        
        conn = self.db_connection()
        cur = conn.cursor()
        for table in tables:
            cur.execute(table)

        print ("created successfully")
        conn.commit()
        conn.close()
        
    def run(self,sql,data):
        conn = self.db_connection()
        cur = conn.cursor()
        con = cur.execute(sql, data)
        conn.commit()
        conn.close()
        return con

    def getting_one_user(self,sql,data):
        conn = self.db_connection()
        cur = conn.cursor()
        cur.execute(sql, data)
        results = cur.fetchone()
        conn.commit()
        conn.close()
        return results

def initialize():
    db = DbModels()
    db.db_connection()
    db.create_table(tables)

if __name__ == "__main__":
    initialize()
