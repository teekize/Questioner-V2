"""
this module contains the validators to be used in the application

"""
import re

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
    
   def check_if_data_is_whitespace(self, data):
        for input_ in data.values():
            string_to_strip = input_.strip()
            if len(string_to_strip) <= 3:
                return False
    
   def check_if_valid_email(self, data):
        pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if pattern.search(data.get("email")) == None:
            return False

   def check_if_valid_phone_number(self, data):
       """checks if the given data is a valid mobile phone"""
       phone_regex = re.compile(r'\b\d{3} \d{3} \d{4}\b')
	   
       if phone_regex.search(data.get("phonenumber"))== None:
            return False

   def check_is_digit(self, data):
       if type(data.get("phonenumber")) != int:
           return False

   def check_password_strength(self,data):
       if len(data.get("password"))<6:
           return False

