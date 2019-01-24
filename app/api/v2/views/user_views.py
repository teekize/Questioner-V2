from flask import Blueprint, request, jsonify
import jwt
from instance.config import Config
from flask_bcrypt import check_password_hash, generate_password_hash
from app.api.v2.utils.validation import Validators
from app.api.v2.models.user_models import UserModel
from app.api import app_blueprint

validators = Validators()   
user_model = UserModel()

@app_blueprint.route("/auth/signup",methods=["POST"])
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

    to_be_string = (username, password, email, firstname, lastname)

    if validators.check_if_string_(to_be_string) == False:
        return jsonify({"status" : 400, 
                        "error":[{"username": " need to be a string",
                                  "email" : "needs to be a string",
                                  "firstname" : "needs to be string", 
                                  "lastname" :  "needs to be a string", 
                                  "password" : " needs to be a string"
                                }]}),400
    if validators.check_if_valid_email (email)== False:
        return jsonify(
                        {"status":400,
                         "error" : "invalid email address"
                        }
                      ), 400
    if validators.check_password_strength(password) == False:
        return jsonify({
                        "status":400, 
                        "error": "password length should atleast 6 characters long"
                        }),400
    if validators.check_if_valid_phone_number(phonenumber) ==  False:
        return jsonify({
                        "status" : 400,
                        "error" : "phone number should be in the format 020 254 2542"
        }),400
    if user_model.check_for_same_email_username(email, username) == False:
        return jsonify({"error": "the email already exists",
                         "status":409}),409

    # hashed_pass = genpassword)
    user_data = {
                    "username" : username,
                    "password" : password,
                    "email" : email,
                    "firstname" : firstname,
                    "lastname" : lastname,
                    "phonenumber" : phonenumber,
                    "isdamin": isadmin
                }
    user_model_response = user_model.save(user_data)
    return jsonify(user_model_response),201


@app_blueprint.route("/auth/login", methods= ["POST"])
def login_user():
    if not request.json or not "username" in request.json  or not "password" in request.json:
        return jsonify({"error":"username, password are required", "status": 400}),400

    username = request.json["username"]
    password = request.json["password"]

    # if user_model.check_for_same_email_username(username) ==  False:
    #     return jsonify({"error":"user with the username is not found", "status":404}),404
    
    user = user_model.getting_one_user (username)
    if not user:
        return jsonify({"error":"user with the username is not found", "status":404}),404
    
    stored_password = user[6]

    if stored_password != password:
        return jsonify({"error": "invalid password", "status":401}),401

    fields =["user_id", "lastname", "email"]
    keys =[user[0], user[2], user[4]]
    token=jwt.encode({"user_id":user[0], "username":user[5], "email":user[4]}, Config.secret_key)
    return jsonify({"status": 200,
                    "data" :[{"token":token.decode("UTF-8"),
                               "user": dict(zip(fields,keys))
                             }
                            ]
                    })
        