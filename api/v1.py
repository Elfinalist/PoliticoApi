from flask import Blueprint, request

v1 = Blueprint('v1_api', __name__, url_prefix='/api/v1')

@v1.route("/")
def hello():
    return "Hello World!"