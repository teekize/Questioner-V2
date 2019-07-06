import psycopg2
from .sql_queries import tables
from instance.config import config




class DbModels:
    """contains the functions that pertain the database connection"""

    def db_connection(self):
        """this method creates the connection to the database and returns a conn object"""
        conn = psycopg2.connect(config["DATABASE"])
        return conn
    

    def create_table(self, tables):
        """this creates all tables"""
        try:
            conn = self.db_connection()
            cur = conn.cursor()
            for table in tables:
                cur.execute(table)

            print ("created successfully")
            conn.commit()
            conn.close()    
        except(Exception, psycopg2.DatabaseError) as error:
            raise error
    

    
def initialize():
    db = DbModels()
    db.db_connection()
    db.create_table(tables)

if __name__ == "__main__":
    initialize()
