from flask import Blueprint, request, jsonify, g
import json
from functools import wraps
from api.v2.models.politico import Politico
from api.v2.models.user import User
from api.v2.models.errors import InputError, DBError, AuthError
import jwt, os

politico = Politico()
JWT_PASS = 'Ypw,U$f]]Q:lXxlADxqVso6}8p+Qey'
JWT_ALGORITHM = 'HS256'

v2 = Blueprint('v2_api', __name__, url_prefix='/api/v2')

@v2.route("/")
def hello():
    return "Hello World!"

def get_user_id(token):
   user = jwt.decode(token, JWT_PASS, JWT_ALGORITHM)
   g.user_id = user.get('user_id', '0')
   return ['user_id']

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Please login to access this route'}), 401
        try:
            user = get_user_id(token)
        except jwt.DecodeError:
            return jsonify({'message': 'invalid token'}), 401
        g.user = user
        return func(*args, **kwargs)
    return wrapper

def get_user_role(user_id):
    user = User.get(user_id)
    is_admin = user.get_user_role
    return is_admin

def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        has_admin_rights = get_user_role
        if not has_admin_rights:
            return jsonify({'message': 'Please login to access this route'}), 401                
        return func(*args, **kwargs)
    return wrapper

@v2.route("/parties", methods=["POST", "GET"]) 
@login_required
@is_admin
def parties():
    print("Got here")
    response = {}
    if(request.method == 'POST'):
        try:
            party_data = request.json
            party_name = party_data.get("name")
            party_hq = party_data.get("hqAddress")
            party_logo = party_data.get("logoUrl")

            # create political party
            party = politico.create_political_party(
                party_name, party_hq, party_logo)
            response["status"] = 201
            response["data"] = party
            return jsonify(response)
        except InputError as error:
            response["status"] = 400
            response["error"] = error.message
            return jsonify(response), response["status"]

    # get all political parties
    elif(request.method == 'GET'):
        political_parties = politico.get_political_parties()
        response["status"] = 200
        response["data"] = political_parties
        return jsonify(response), response["status"]
    else:
        pass


@v2.route("/parties/<int:id>", methods=["GET", "DELETE", "PUT"])
@login_required
def party(id):
    response = {}
    # get one party
    if(request.method == 'GET'):
        p_party = politico.get_political_party(id)
        if(len(p_party) == 0):
            response["status"] = 404
            response["error"] = "political party not found"
        else:
            response["status"] = 200
            response["data"] = p_party
        return jsonify(response), response["status"]
    # delete party
    elif(request.method == 'DELETE'):
        deleted = politico.delete_political_party(id)
        if(deleted):
            response["status"] = 200
            response["data"] = {
                "message": "political party sucessfully deleted"
            }
        else:
            response["status"] = 404
            response["error"] = "political party not found"
        return jsonify(response), response["status"]
    elif(request.method == 'PUT'):
        try:
            party_data = request.json
            new_name = party_data["name"]
            response_data = politico.edit_political_party(id, new_name)
            response["status"] = 200
            response["data"] = response_data
            return jsonify(response), response["status"]
        except InputError as error:
            response["status"] = 404
            response["error"] = error.message
            return jsonify(response), response["status"]


@v2.route("/offices", methods=["POST", "GET"])
def office():
    response = {}
    if (request.method == 'POST'):
        try:
            office_data = request.json
            office_name = office_data.get("name")
            office_type = office_data.get("office_type")
            # create political office
            office = politico.create_political_office(office_name, office_type)
            response["status"] = 201
            response["data"] = office
            return jsonify(response), response["status"]
        except InputError as error:
            response["status"] = 400
            response["data"] = error.message
            return jsonify(response), response["status"]
    # get all political offices
    elif(request.method == 'GET'):
        political_offices = politico.get_political_offices()
        response["status"] = 200
        response["data"] = political_offices
        return jsonify(response), response["status"]
    else:
        pass


@v2.route("/offices/<int:id>", methods=["GET", "DELETE", "PUT"])
def get_office(id):
    response = {}
    # get one office
    if (request.method == "GET"):
        p_office = politico.get_political_office(id)
        if(len(p_office) == 0):
            response["status"] = 404
            response["error"] = "political party not found"
        else:
            response["status"] = 200
            response["data"] = p_office
        return jsonify(response), response["status"]

    elif (request.method == "DELETE"):
        deleted = politico.delete_political_office(id)
        if(deleted):
            response["status"] = 200
            response["data"] = {
                "message": "political office sucessfully deleted"
            }
        else:
            response["status"] = 404
            response["error"] = "political office not found"
        return jsonify(response), response["status"]
    elif (request.method == "PUT"):
        try:
            office_data = request.json
            new_name = office_data["name"]
            response_data = politico.edit_political_office(id, new_name)
            response["status"] = 200
            response["data"] = response_data
            return jsonify(response), response["status"]
        except InputError as error:
            response["status"] = 404
            response["error"] = error.message
            return jsonify(response), response["status"]


@v2.route("/auth/signup", methods=["POST"])
def signup():
    response = {}
    try:
        user_data = request.json
        name = user_data.get("name")
        password = user_data.get("password")
        email = user_data.get("email")
        c_password = user_data.get("confirm_password")
        user = politico.create_user(name, email, password, c_password)
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


@v2.route("/auth/login", methods=["POST"])
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
