from flask import jsonify, make_response
from app.api  import app_blueprint

@app_blueprint.errorhandler(405)
def method_not_allowed(error):
    """Error response message for method not allowed"""
    return make_response(jsonify({"message": "method not allowed"}),405)

@app_blueprint.errorhandler(500)
def server_error(error):
    """Error response message for server error"""
    return make_response(jsonify({"message": "Internall error"}),500)

@app_blueprint.errorhandler(404)
def not_found(error):
    """Error response message for not found"""
    return make_response(jsonify({"message": "request not found"}),404)

@app_blueprint.errorhandler(403)
def access_forbiden(error):
    """Error response message for access forbiden"""
    return make_response(jsonify({"message": "access denied"}),403)

@app_blueprint.errorhandler(400)
def bad_request(error):
    """Error response message for a bad request"""
    return make_response(jsonify({"message": "bad request"}), 400)