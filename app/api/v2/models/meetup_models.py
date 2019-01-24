from app.api.v2.database.database import DbModels
from app.api.v2.database.sql_queries import create_meetup,check_same_meetup_name,get_meetup_by_id
import datetime
from psycopg2 import IntegrityError


class MeetUpModel(DbModels):
    """conatins methids for the meetup models"""

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
                    "user": dict(zip(keys,response_from_db)),
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

        if not result :
            return False

    def check_for_meetup_by_id(self, data):
        try:
            conn = self.db_connection()
            cur = conn.cursor()
            cur.execute(get_meetup_by_id, (data,))
            results = cur.fetchone()
            conn.commit()
            conn.close()

            """meetup_id createdon| location images topic happeningon tags name createdby"""
            values= (results[0], results[2], results[4], results[5], results[6])
            keys=["meetup_id", "location", "topic", "happeningon", "tags"]
            return {
                    "status": 200,
                    "data": [ dict(zip(keys, values))]
                    }
        except TypeError:
            return {
                    "error":"could not find meetup with that id",
                     "status":404
                     }

