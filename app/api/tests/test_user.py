from app import create_app
from flask import jsonify, json
from instance.config import config
import unittest

class UserTests(unittest.TestCase):
    """ adds the tests for the user class"""
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client= self.app.test_client()

        self.user= {
                    "username":"kanyabfeff",
                    "email" :"tindereuef@gmail.com",
                    "firstname": "teekize",
                    "lastname" : "lemein",
                    "password": "hawwaala",
                    "phonenumber": "079 879 5451",
                    "isadmin": "False"
                   }


    def test_user_signup(self):
        """tests the user signup"""
        response = self.client.post("/api/v2/signup", data =json.dumps(self.user), content_type = "application/json")
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        self.app = None
    