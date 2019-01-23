from app import createapp
from instance import config

class UserTests:
    """ adds the tests for the user class"""
    def setup(self):
        self.app = create_app(config.Testing)
        self.client= self.app.test_client()

        self.user= {
                    "username":"kanyabf",
                    "email" :"tinderd@gmail.com",
                    "firstname": "teekize",
                    "lastname" : "lemein",
                    "password": "hawwaala",
                    "phonenumber": "079 879 5451",
                    "isadmin": "False"
                   }


    def test_user_signup(self):
        """tests the user signup"""
        response = self.client.post("/signup", data = self.user, content_type = "application/json")


    