from flask import Blueprint, request, jsonify
from instance.config import Config
from app.api.v2.utils.validation import Validators,token_required
from app.api.v2.models.question_models import QuestionModel

validators = Validators()
question = QuestionModel()
question_blueprint = Blueprint("question_blueprint",__name__)

@question_blueprint.route("/questions", methods=["POST"])
@token_required
def create_question(username):
    if not request.json:
        return jsonify(
                        {
                        "message": "request should be in json format",
                         "status": 400
                         }
                         ),400

    "question_id | createdon | createdby | meetup | title | body | votes"

    data = request.json
    required_fields = "meetup", "title", "body"
    response = validators.check_required_fields(data, required_fields)
    if response == False:
        return jsonify(response),400
    title = request.json["title"]
    body = request.json["body"]
    meetup = request.json["meetup"]
    to_be_string= title,body
    all_fields = title,body

    
    if validators.check_if_string_(to_be_string)==False:
        return jsonify({"status": 400, "error": "the fields body and title need to be strings"}),400

    if validators.check_not_empty(all_fields)==False:
        return jsonify({"status":400, "error": "the fields body, title and meetup should not be empty"}),400

    question_from_user =[username[1],title,body,meetup]
    
    """we then check if there is a meetup with that id that exists"""
    # select meetup id if meetup id=given meetup id
    meetup_exist = question.check_meetup_exist(meetup)
    if meetup_exist["status"] == 404:
        return jsonify(meetup_exist),404

    response = question.save_question(question_from_user)
    if response["status"]==409:
        return jsonify(response),409
    elif response["status"]==201:
        return jsonify(response),201

@question_blueprint.route("/questions", methods=["GET"])
def get_all_questions():
    response = question.get_all_questions()
    return jsonify(response),200

@question_blueprint.route("/questions/<int:question_id>/upvote", methods=["PATCH"])
@token_required
def upvote_question(username, question_id):
    """check if that question exists exists"""
    results = question.check_if_question_exists(question_id, username)
    if results == False:
        return jsonify({"error": "question with that id not found"}), 404


    """check if a question with that id exists in a given question"""
    """we then get the votes of the question , and upvote the votes by one"""
    response = question.update_question_votes(question_id, username, "u")


    """after the question is upvoted by a user we are going to insert the question_id and userid in the 
    a blacklisted votes table"""
    if response["status"] !=200:
        
        return jsonify(response), 403
    return jsonify(response), 200
    


@question_blueprint.route("/questions/<int:question_id>/downvote", methods=["PATCH"])
@token_required
def downvote_question(username, question_id):
    """check if a question with that id exists"""
    results = question.check_if_question_exists(question_id, username)
    if results == False:
        return jsonify({"error": "question with that id not found"}), 404

    response = question.update_question_votes(question_id, username, "d")


    """after the question is downvoted by a user we are going to insert the question_id and userid in the 
    a blacklisted votes table"""
    if response["status"] !=403:
        
        return jsonify(response), 200
    return jsonify(response), 403


"""
here we have the comments from the users,
the comment will have a question_id with which the question actually was asked
"""
@question_blueprint.route("/comments/", methods=["POST"])
@token_required
def create_comment(username):
    if not request.json:
        return jsonify(
                        {
                        "message": "request should be in json format",
                         "status": 400
                         }
                         ),400

    """createdby INT REFERENCES users(user_id),
        meetup INT REFERENCES meetups(meetup_id),
        title varchar(40) UNIQUE NOT NULL,
        body VARCHAR(60) NOT NULL,
        question I"""

    data = request.json
    required_fields = "meetup", "title", "body","question_id"
    response = validators.check_required_fields(data, required_fields)
    if response == False:
        return jsonify(response),400
    title = request.json["title"]
    body = request.json["body"]
    meetup = request.json["meetup"]
    question_id = request.json["question_id"]
    to_be_string= title,body
    all_fields = title,body

    """we then check if there is a meetup with that id that exists"""
    # select meetup id if meetup id=given meetup id
    meetup_exist = question.check_meetup_exist(meetup)
    if meetup_exist["status"] == 404:
        return jsonify(meetup_exist),404

    """check if a question with that id exists"""
    response = question.check_if_question_exists(question_id, username)
    if response == False:
        return jsonify({"status":404, "message": "question with that id does not exists"}), 404
    
    if validators.check_if_string_(to_be_string)==False:
        return jsonify({"status": 400, "error": "the fields body and title need to be strings"}),400

    if validators.check_not_empty(all_fields)==False:
        return jsonify({"status":400, "error": "the fields body, title and meetup should not be empty"}),400

    comment_from_user =[ username[1],title,body,meetup,question_id]
    
   
    response = question.create_comment(comment_from_user)
    if response["status"]==409:
        return jsonify(response),409
    elif response["status"]==201:
        return jsonify(response),201