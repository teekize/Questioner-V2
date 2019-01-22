from flask import Blueprint, request, jsonify

user_blueprint= Blueprint("user_blueprint", __name__, url_prefix="/api/v2/auth/")


@user_blueprint.route("/signup",methods=["POST"])
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