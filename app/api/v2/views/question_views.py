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

    question_from_user ={
                "createdby":username[1],
                "title": title,
                "body": body,
                "meetup": meetup
    }
    
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
