from flask import Blueprint, request, jsonify
from api.v2.models.user import User
from api.v2.models.errors import InputError, DBError, AuthError
from api.v2.helpers.decorators import login_required, is_admin
from api.v2.models.user import User
from api.v2.models.politico import Politico

politico = Politico()

v2_party = Blueprint('v2_api_parties', __name__, url_prefix='/api/v2/parties')

@v2_party.route("", methods=["POST", "GET"]) 
@login_required
def parties():
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


@v2_party.route("/<int:id>", methods=["GET", "DELETE", "PUT"])
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