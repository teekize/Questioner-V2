""" this module contains all the user functions to interact with the database"""
from ..database.sql_queries import (save_user, get_a_user_email,get_a_user_by_username,
                                     get_user_by_id,geta_user_by_username, alter_table_user)
from ..database.database import DbModels
import datetime
from psycopg2 import IntegrityError,sql
from psycopg2.extras import RealDictCursor


class UserModel(DbModels):
    """ contains the user models"""
    def __init__(self):
        self.createdon = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')

    def check_for_same_email_username(self,email, username):
        """could check for same email or password"""
        results= None
        if email:
            conn = self.db_connection()
            cur = conn.cursor()
            cur.execute(get_a_user_email, (email,))
            results = cur.fetchone()
            conn.commit()
            cur.close()
            

            if results is not None:
                return False,
        if username:
            conn = self.db_connection()
            cur = conn.cursor()
            cur.execute(get_a_user_by_username, (username,))
            results = cur.fetchone()
            conn.commit()
            cur.close()
            

            if results is not None:
                return False, results
        
   
    def save(self, data):
        firstname = data.get("firstname"),
        lastname = data.get("lastname"),
        othername = data.get("othername", ""),
        email = data.get("email"),
        username = data.get("username"),
        password = data.get("password"),
        
        registered = self.createdon
        """first_name, last_name, othername, email,user_name, password, isadmin, registered)"""
        

        new_user = ( firstname, lastname, othername, email, username, password, registered
                   )
        try:
            conn = self.db_connection()
            cur = conn.cursor()
            cur.execute(save_user, new_user)
            results = cur.fetchone()
            conn.commit()
            cur.close()
            
            keys = ["user_id","username","email","password"]
            user = dict(zip(keys, results))
            print(results)


            return {"status":201, "data": [
                                            {"user": user,
                                            "message": "user sucessfully created"
                                            },
                                        ]}
        except IntegrityError:
            return ({"error":"user with same username and email exists", "status":409})
    def getting_one_user(self, data):
        """user_name,user_id returns this values"""
        # get_a_user_by_username, (data,)
        conn = self.db_connection()
        cur = conn.cursor()
        cur.execute(get_a_user_by_username, (data,))
        results = cur.fetchone()
        conn.commit()
        conn.close()
        print(results)
        return results

    def get_one_user_with_username(self, data):
        """this returns everything about the user"""
        # geta_user_by_username, (data,)
        conn =self.db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(geta_user_by_username, (data,))
        results =cur.fetchone()
        conn.commit()
        conn.close()
        return results

    
                    