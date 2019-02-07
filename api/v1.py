from flask import Blueprint, request, jsonify
import json
from api.models import Politico, InputError

politico = Politico()

v1 = Blueprint('v1_api', __name__, url_prefix='/api/v1')

@v1.route("/")
def hello():
    return "Hello World!"


@v1.route("/parties", methods=["POST", "GET"])
def parties():
    response = {}
    if(request.method == 'POST'):
        try:
            party_data = request.json
            party_name = party_data["name"]
            party_hq = party_data["hqAddress"]
            party_logo = party_data["logoUrl"]

            # create political party
            party = politico.create_political_party(party_name, party_hq, party_logo)
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

@v1.route("/parties/<int:id>", methods=["GET", "DELETE", "PUT"])
def party(id):
    response = {}
    #get one party
    if(request.method == 'GET'):
        p_party = politico.get_political_party(id)
        if(len(p_party) == 0):
            response["status"] = 404
            response["error"] = "political party not found"
        else:
            response["status"] = 200
            response["data"] = p_party
        return jsonify(response), response["status"]
    #delete party
    elif(request.method =='DELETE'):
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


@v1.route("/offices", methods=["POST", "GET"])
def office():
    response = {}
    if (request.method == 'POST'):
        try:
            office_data = request.json
            office_name = office_data["name"]
            office_type = office_data["office_type"]
            #create political office
            office = politico.create_political_office(office_name,office_type)
            response ["status"] = 201
            response ["data"] = office
            return jsonify(response), response["status"]
        except InputError as error:
            response ["status"] = 400
            response ["data"] = error.message
            return jsonify(response), response["status"]



