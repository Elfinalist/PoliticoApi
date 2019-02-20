import json
from flask import request, jsonify, Blueprint
from api.v2.models.user import User
from api.v2.models.politico import Politico
from api.v2.models.errors import InputError, DBError, AuthError

politico = Politico()
v2_authentication = Blueprint('v2_api_auth', __name__, url_prefix='/api/v2/auth')

@v2_authentication.route("/")
def hello():
    return "Hello World!"

@v2_authentication.route("/signup", methods=["POST"])
def signup():
    response = {}
    try:
        user_data = request.json
        name = user_data.get("name")
        password = user_data.get("password")
        email = user_data.get("email")
        c_password = user_data.get("confirm_password")
        is_admin = user_data.get("is_admin")
        user = politico.create_user(name, email, password, c_password, is_admin)
        del user["password"]
        response["status"] = 201
        response["data"] = {
            "token": user.create_token(),
            "user": user
        }
        return jsonify(response), response["status"]
    except InputError as error:
        response["status"] = 400
        response["error"] = error.message
        return jsonify(response), response["status"]
    except DBError as error:
        response["status"] = 500
        response["error"] = error.message
        return jsonify(response), response["status"]
    except Exception as error:
        print(error)
        response["status"] = 500
        response["error"] = "An unknown error occured"
        return jsonify(response), response["status"]

@v2_authentication.route("/login", methods=["POST"])
def login():
    response = {}
    try:
        user_data = request.json
        email = user_data.get("email")
        password = user_data.get("password")
        user = politico.login(email, password)
        del user["password"]
        response["status"] = 200
        response["data"] = {
            "token": user.create_token(),
            "user": user
        }
        return jsonify(response), response["status"]
    except InputError as error:
        response["status"] = 404
        response["error"] = error.message
        return jsonify(response), response["status"]
    except AuthError as error:
        response["status"] = 401
        response["error"] = error.message
        return jsonify(response), response["status"]
    except Exception as error:
        print(error)
        response["status"] = 500
        response["error"] = "An unknown error occured"
        return jsonify(response), response["status"]