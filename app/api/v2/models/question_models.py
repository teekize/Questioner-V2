from app.api.v2.database.database import DbModels
from app.api.v2.database.sql_queries import (save_question,get_meetup_by_id, 
                                            get_question_by_id, get_all_questions, update_votes, insert_blacklisted,
                                            check_if_blacklisted)
import datetime
from psycopg2 import IntegrityError
from psycopg2.extras import RealDictCursor

"""this file conatins the questions methods that are called by the view"""
class QuestionModel(DbModels):
    """class containing the questionmodel methods"""
    
    def __init__(self):
        self.day_created = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M')

    "question_id | createdon | createdby | meetup | title | body | votes"
    def get_all_questions(self):
        conn = self.db_connection()
        cur =conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(get_all_questions,)
        results = cur.fetchall()
        conn.commit()
        conn.close()

        return results

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
            conn.commit()
            conn.close()

            return {
                    "status":201,
                    "data": results
                  }
        except IntegrityError:
            return {
                "status":409,
                "error":"a simillar question has been asked with same "
            }

    def check_meetup_exist(self, meetup_id):
        conn = self.db_connection()
        cur = conn.cursor()
        cur.execute(get_meetup_by_id, (meetup_id,))
        results = cur.fetchone()
        conn.commit()
        conn.close()
        if results:
            return{"status":200}
        else:
            return{
                    "status":404,
                    "error":"could not find meetup with that id"
                    }
       
    def check_if_question_exixts(self, data, username):
        """this function checks if the question exists in the database
        takes in the parameter data which is the qustion id 
        it then returns the false is the results variable is none and 
        true is its found
        """
        # person = username[1]
        conn = self.db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(get_question_by_id, (data,))
        results = cur.fetchone()
        conn.commit()
        conn.close()
        

        if not results:
            return False
        else :
            return results

    def update_question_votes(self, question_id, username, identifier):
        """
        its the function that update the questions votes
        takes three parameeters question_id, username and the and identifier"
        the identifier can be ethier (d, u) symbolising d- downvote and u- for upvote

        """

        user_id = username[1]
        print (user_id)

        question = self.check_if_question_exixts(question_id, username)
        blacklisted = self.check_if_user_and_question_blacklisted(user_id, question_id)


        if blacklisted:
            return {
                     "message": "you cannot vote twice",
                     "status": 403
                    }

        if identifier=="u":
            new_vote = question["votes"]+1
            conn = self.db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(update_votes, (new_vote, question_id))
            results = cur.fetchone()
            conn.commit()
            conn.close()

            results["message"]="you have upvoted the question"
            results["status"] = 200
        elif identifier == "d":
            new_vote = question["votes"]-1
            conn = self.db_connection()
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(update_votes, (new_vote, question_id))
            results = cur.fetchone()
            conn.commit()
            conn.close()

            results["message"]="you have downvoted the question"
            results["status"] = 200
        

        """after the upvote we then added the user_id and question_id into the blacklisted_users and questions"""
        self.blacklisted_users(user_id, question_id)
        return (results)

    def blacklisted_users(self, user_id, question_id):
        conn = self.db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(insert_blacklisted, (user_id, question_id))
        results = cur.fetchone()
        conn.commit()
        conn.close()

        return results

    def check_if_user_and_question_blacklisted(self, user_id, question_id):
        conn = self.db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(check_if_blacklisted, (user_id, question_id))
        results = cur.fetchone()
        conn.commit()
        conn.close()

        return results