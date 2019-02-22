from flask import Blueprint, request, jsonify
from api.v2.models.user import User
from api.v2.models.errors import InputError, DBError, AuthError
from api.v2.helpers.decorators import login_required, is_admin
from api.v2.models.user import User
from api.v2.models.politico import Politico

politico = Politico()

v2_candidate = Blueprint('v2_candidate', __name__, url_prefix='/api/v2/office')

@v2_candidate.route("/<int:user_id>/register", methods=["POST"])
@login_required
@is_admin
def register_candidate(user_id):
    response = {}
    if request.method == 'POST':
        try:
            candidate_data = request.json
            office_id = candidate_data.get("office_id")
            #create candidate
            candidate = politico.create_candidate(user_id, office_id)
            response["status"] = 201
            response["data"] = candidate
            return jsonify(response)
        except InputError as error:
            response["status"] = 400
            response["error"] = error.message
            return jsonify(response), response["status"]