from app.api.v2.database.database import DbModels
from app.api.v2.database.sql_queries import save_question,get_meetup_by_id
import datetime
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor

"""this file conatins the questions methods that are called by the view"""
class QuestionModel(DbModels):
    """class containing the questionmodel methods"""
    def __init__(self):
        self.day_created = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')

    "question_id | createdon | createdby | meetup | title | body | votes"


    def save_question(self, data):
        try:
            createdon =self.day_created
            createdby = data["createdby"]
            meetup = data["meetup"]
            title = data["title"]
            body = data["body"]

            data_to_pass = (title,body,meetup, createdon, createdby)
            conn = self.db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(save_question,(data_to_pass))
            results = cur.fetchone()

            return {
                    "status":201,
                    "data": results
                  }
        except IntegrityError:
            return {
                "status":409,
                "error":"a simillar question has been asked with same title"
            }

    def check_meetup_exist(self, meetup_id):
        try:
            conn = self.db_connection()
            cur = conn.cursor()
            cur.execute(get_meetup_by_id, (meetup_id,))
            results = cur.fetchone()
            conn.commit()
            conn.close()

            return{"status":200}
        except TypeError:
            return {
                    "error":"could not find meetup with that id",
                     "status":404
                     }
