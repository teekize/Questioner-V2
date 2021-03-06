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
    

    to_be_string = (username, password, email, firstname, lastname)
    to_not_be_empty =(username, password, email, firstname, lastname, phonenumber)

    if validators.check_if_string_(to_be_string) == False:
        return jsonify({"status" : 400, 
                        "error":[{"username": " need to be a string",
                                  "email" : "needs to be a string",
                                  "firstname" : "needs to be string", 
                                  "lastname" :  "needs to be a string", 
                                  "password" : " needs to be a string"
                                }]}),400
    if validators.check_not_empty(to_not_be_empty):
        return jsonify({"error": "the fields should not be empty", "status":400}),400
    
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
   
    user_data = {
                    "username" : username,
                    "password" : password,
                    "email" : email,
                    "firstname" : firstname,
                    "lastname" : lastname,
                    "phonenumber" : phonenumber,
                    
                }
    if validators.check_if_data_is_whitespace(user_data) == False:
        return jsonify({"error":" fields cannot be whitspaces", "status":400}),400
    user_model_response = user_model.save(user_data)
    if user_model_response["status"]==409:
        return jsonify(user_model_response),409
    elif user_model_response["status"]==201:
        return jsonify(user_model_response),201


@app_blueprint.route("/auth/login", methods= ["POST"])
def login_user():
    if not request.json or not "username" in request.json  or not "password" in request.json:
        return jsonify({"error":"username, password are required", "status": 400}),400

    username = request.json["username"]
    password = request.json["password"]
    
    user = user_model.get_one_user_with_username (username)
    if not user:
        return jsonify({"error":"user with the username is not found", "status":404}),404
        
    print (user)
    
    stored_password = user["password"]

    if stored_password != password:
        return jsonify({"error": "invalid password", "status":401}),401

    fields =["user_id", "lastname", "email"]
    keys =[user["user_id"], user["last_name"], user["email"]]
    token=jwt.encode({"user_id":user["user_id"], "username":user["user_name"], "email":user["email"]}, Config.secret_key)
    return jsonify({"status": 200,
                    "data" :[{"token":token.decode("UTF-8"),
                               "user": dict(zip(fields,keys))
                             }
                            ]
                    })
        