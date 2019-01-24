from app.api.v2.database.database import DbModels
from app.api.v2.database.sql_queries import create_meetup,check_same_meetup_name
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

