"""
this module contains the validators to be used in the application

"""
import re
from flask import request, jsonify
import  jwt
from instance.config import Config
from functools import wraps
from app.api.v2.models.user_models import UserModel
import datetime

user_model = UserModel()

class Validators:
   """contails the methods for the validators class"""

   def check_if_string_(self, information):
       """checks if data given is a string"""
       for data in information:
           if type (data) != str:
               return False

   def check_not_empty(self, data):
        """checks that the data is not empty"""
        for value in data:
            if len(value) == 0:
                return False
    
   def check_if_data_is_whitespace(self, data=None, itereable=None):
       if data: ### check on thiss
            for input_ in data.values():
                string_to_strip = input_.strip()
                if len(string_to_strip)==0:
                    return False

       if itereable:
            for data in itereable:
                string_to_strip = data.strip()
                if len(string_to_strip)==0:
                    return False
    
   def check_if_valid_email(self, email):
        pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if pattern.search(email) == None:
            return False

   def check_if_valid_phone_number(self, number):
       """checks if the given data is a valid mobile phone"""
       phone_regex = re.compile(r'\b\d{3} \d{3} \d{4}\b')
	   
       if phone_regex.search(number) == None:
            return False

   def check_is_digit(self, data):
       if type(data.get("phonenumber")) != int:
           return False

   def check_password_strength(self, password):
       if len(password)<6:
           return False


   def check_required_fields(self, data, required_field):
        for field in required_field:
            if field not in data:
                return False, {"message": "{}, {}, {}, {} are"
                        "required".format(required_field[0],required_field[1],
                        required_field[2],required_field[3])}
            

   def check_date_if_matches(self, data):
        date = data["happeningon"]
        
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d %H:%M')
        except ValueError:
            return False

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token=None
	
        if 'x-access-token' in request.headers:
            token=request.headers["x-access-token"]
            print(request.headers["x-access-token"])

        if not token:
            return jsonify({"message":"token is missing", "status":403}),403

        else:
            data=jwt.decode(token,Config.secret_key)
            current_user= user_model.getting_one_user(data["username"])#[user for user in users if user["name"]==data["username"]]
            username= current_user
            
		
            # return jsonify({"message":"token is invalid"})
        return f(username, *args, **kwargs)
    return decorated