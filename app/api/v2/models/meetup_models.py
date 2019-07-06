from app.api.v2.database.database import DbModels
from app.api.v2.database.sql_queries import (create_meetup,check_same_meetup_name,
                                                get_meetup_by_id,get_upcoming_meetups, create_rsvp,
                                                created_by_admin, delete_meetup_by_id)
import datetime
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor


class MeetUpModel(DbModels):
    """conatins methids for the meetup models"""

    # def __init__():
    #     self.response ={}

    def save_meetup(self, data):
        conn = self.db_connection()
        cur = conn.cursor()

        name = data["name"],
        topic= data["topic"],
        location=data["location"],
        happeningon= data["happeningon"],
        tags = data["tags"],
        images= data["images"]
        createdby =data["createdby"]
        createdon = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        """createdon, location,images,topic,
                happeningon,tags,name,createdby"""
        try:
            data=(createdon,location,images,topic,happeningon,tags,name,createdby,)
            cur.execute(create_meetup, data)
            response_from_db = cur.fetchone()
            conn.commit()
            cur.close()

            keys =["meetup_id", "name", "happeningon"]
            return {
                    "message": "successfully created",
                    "data": dict(zip(keys,response_from_db)),
                    "status":201
                    }
        except IntegrityError:
            return{
                    "error":"meetup with same topic exists", 
                    "status":409
                    }

    def check_same_meetup(self, name):
        conn = self.db_connection()
        cur = conn.cursor()
        cur.execute(check_same_meetup_name, (name,))
        result = cur.fetchone()
        conn.commit()
        conn.close()

        if not result :
            return False
       

    def check_for_meetup_by_id(self, data):
        # try:
        conn = self.db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(get_meetup_by_id, (data,))
        results = cur.fetchone()
        conn.commit()
        conn.close()

        if results:


            """meetup_id createdon| location images topic happeningon tags name createdby"""
        # values= (results[0], results[2], results[4], results[5], results[6])
        # keys=["meetup_id", "location", "topic", "happeningon", "tags"]
        # [ dict(zip(keys, values))]
            return {
                    "status": 200,
                    "data": results
                    }
    # except TypeError:
        else:
            return {
                    "error":"could not find meetup with that id",
                    "status":404
                    }

    def get_upcoming_meetups(self):
        data= datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')
        conn = self.db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(get_upcoming_meetups,(data,))

        results = cur.fetchall()
        conn.commit()
        conn.close()
    
        return {
                "status":200,
                 "data" : results
                }

    def rsvp_meetup(self, data):
        """creates the rsvp for a meetup"""
        new_entries = data[0], data[1], data[2]
        conn =self.db_connection()
        cur =conn.cursor(cursor_factory= RealDictCursor)
        cur.execute(create_rsvp, new_entries)
        results= cur.fetchone()
        conn.commit()
        conn.close()

        return{
            "status":200,
            "data": results
        }

    def get_meetup_by_admin_id(self, admin_id, meetup_id):
        """takes the meetup id and admin  id and checks if he is the one who created the meetup"""
        """we check if that meetup exists first"""
        response =self.check_for_meetup_by_id(meetup_id)
        if  response["status"] != 200:
            return response
        
        if response["data"]["createdby"] != admin_id:
            return {
                    "message": "ooops you cannot delete an meetup you never created",
                    "status": 403
                    }
        else:
            
            conn = self.db_connection()
            cur =conn.cursor(cursor_factory= RealDictCursor)
            cur.execute(delete_meetup_by_id, (meetup_id,))
            conn.commit()
            conn.close()

            response =self.check_for_meetup_by_id(meetup_id)
            if  response["status"] != 200:
                return {"message": "meetup successfully deleted",
                        "status": 200
                        }