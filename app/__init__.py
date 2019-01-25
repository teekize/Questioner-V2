from flask import Flask
from app.api.v2.database.database import initialize
from app.api.v2.views.user_views import app_blueprint
from app.api.v2.views.meetup_views import meetup_blueprint
from app.api.v2.views.question_views import question_blueprint
from app.api.v2.utils.hanlders import method_not_allowed, not_found, bad_request, access_forbiden, server_error
from instance.config import config

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.register_blueprint(app_blueprint)
    app.register_blueprint(meetup_blueprint)
    app.register_blueprint(question_blueprint)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(500, server_error)
    app.register_error_handler(404, not_found)
    app.register_error_handler(403, access_forbiden)

    initialize()
    return app

