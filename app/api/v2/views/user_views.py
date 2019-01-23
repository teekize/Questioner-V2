from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash
from app.api.v2.utils.validation import Validators
from app.api.v2.models.user_models import UserModel
from app.api import app_blueprint

validators = Validators()   
user_model = UserModel()
@app_blueprint.route("/signup",methods=["POST"])
def create_user():
    data = request.json
    required_fields = ("username", "password", "email", "firstname", "lastname", "phonenumber")
    for field in required_fields:
        if field not in data:
            return jsonify({"error" : [
                                {
                                 "username" : "Field required",
                                 "password" : "Field required",
                                 "email" : "Field required",
                                 "firstname" : "Field required",
                                 "lastname" : "Field required",
                                 "phonenumber" : "Field required"
                                 }
                              ],
                     "status" : 400
                    }), 400

    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    firstname = data.get("email")
    lastname = data.get("lastname")
    phonenumber = data.get("phonenumber")
    isadmin = data.get("isadmin")

    hashed_pass= generate_password_hash(password)
    user_data = {
                    "username" : username,
                    "password" : hashed_pass,
                    "email" : email,
                    "firstname" : firstname,
                    "lastname" : lastname,
                    "phonenumber" : phonenumber,
                    "isdamin": isadmin
                }

    if user_model.check_for_same_email(user_data) == False:
        return jsonify({"error": "the email already exists",
                         "status":409}),409

    if user_model.check_for_same_username(user_data) == False:
        return jsonify({"error": "the same username already exists", 
                        "status":409}
                    ),409


    to_be_string = (username, password, email, firstname, lastname)

    
    if validators.check_if_string_(to_be_string) == False:
        return jsonify({"status" : 400, 
                        "error":[{"username": " need to be a string",
                                  "email" : "needs to be a string",
                                  "firstname" : "needs to be string", 
                                  "lastname" :  "needs to be a string", 
                                  "password" : " needs to be a string"
                                }]}),400

    if validators.check_if_valid_email (user_data)== False:
        return jsonify(
                        {"status":400,
                         "error" : "invalid email address"
                        }
                      ), 400

    if validators.check_password_strength(user_data) == False:
        return jsonify({
                        "status":400, 
                        "error": "password length should atleast 6 characters long"
                        }),400
                    
    if validators.check_if_valid_phone_number(user_data) ==  False:
        return jsonify({
                        "status" : 400,
                        "error" : "phone number should be in the format 020 254 2542"
        }),400

   
    user_model_response = user_model.save(user_data)
    return jsonify(user_model_response),201