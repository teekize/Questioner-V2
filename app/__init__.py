from flask import Flask
from app.api.v2.database.database import initialize

def create_app():
    app = Flask(__name__)
    initialize()
    return app