from flask import Blueprint, request, jsonify
from instance.config import Config
from app.api.v2.utils.validation import Validators,token_required
from app.api.v2.models.meetup_models import MeetUpModel
from app.api import app_blueprint

validators = Validators()
meetup =MeetUpModel()
meetup_blueprint = Blueprint("meetup_blueprint",__name__)

@meetup_blueprint.route("/meetups", methods=["POST"])
@token_required
def create_meetup(username):
    if not request.json:
        return jsonify({"message": "request should be in json format", "status": 400}),400

    data = request.json
    required_fields = "name", "topic", "location", "happeningon"
    response = validators.check_required_fields(data, required_fields)
    if response == False:
        return jsonify(response),400

    data = {
        "name": request.json["name"],
        "topic" : request.json["topic"],
        "location":request.json["location"],
        "happeningon":request.json["happeningon"],
        "tags" : request.json["tags"],
        "images": request.json["images"],
        "createdby" : username[1]
    }
    data_ ={
            "name": request.json["name"],
            "topic" : request.json["topic"],
            "location":request.json["location"],
            "happeningon":request.json["happeningon"]
    }

    if validators.check_if_data_is_whitespace(data_) ==False:
        return jsonify({"error":"the fields name, topic,"
                         "location and happeningon should not be empty", 
                         "status":400}), 400
    if validators.check_date_if_matches(data) == False:
        return jsonify({
                        "error": "the date needs to be in the format Y-m-d H:M ",
                        "status" : 400
                        }),400

    response = meetup.save_meetup(data)
    if response["status"]== 409:
        return jsonify(response),409
    elif response["status"]==201:
        return jsonify(response),201
    
    