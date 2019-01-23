""" this module contains all the user functions to interact with the database"""
from ..database.sql_queries import save_user, get_a_user_email,get_a_user_by_username
from ..database.database import DbModels
import datetime
from psycopg2 import IntegrityError

class UserModel(DbModels):
    """ contains the user models"""
    def __init__(self):
        self.createdon = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')

    def check_for_same_email(self, data):
        
        email = data.get("email")
        
        conn = self.db_connection()
        cur = conn.cursor()
        cur.execute(get_a_user_email, (email,))
        results = cur.fetchone()

        if results is not None:
            return False
        
    def check_for_same_username(self,data):
        username = data.get("username")
        conn =self.db_connection()
        cur = conn.cursor()
        cur.execute(get_a_user_by_username, (username,))
        results = cur.fetchone()
        if results is not None:
            return False

    def save(self, data):
        firstname = data.get("firstname"),
        lastname = data.get("lastname"),
        othername = data.get("othername", ""),
        email = data.get("email"),
        username = data.get("username"),
        password = data.get("password"),
        isadmin = data.get("isadmin"),
        registered = self.createdon
        

        new_user = ( firstname, lastname, othername, email, username, password, isadmin, registered
                   )
        
        conn = self.db_connection()
        cur = conn.cursor()
        cur.execute(save_user, new_user)
        results = cur.fetchone()
        conn.commit()
        cur.close()
        
        keys = ["user_id", "username" ,"email", "firstname" ]
        results
        user = dict(zip(keys, results))


        return {"status":201, "data": [
                                        {"user": user,
                                        "message": "user sucessfully created"
                                        },


                                      ]}

    def getting_one_user(self,sql,data):
        conn = self.db_connection()
        cur = conn.cursor()
        cur.execute(sql, data)
        results = cur.fetchone()
        conn.commit()
        conn.close()
        return results

                    