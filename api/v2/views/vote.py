from flask import Blueprint, request, jsonify
from api.v2.models.user import User
from api.v2.models.errors import InputError, DBError, AuthError
from api.v2.helpers.decorators import login_required
from api.v2.models.user import User
from api.v2.models.politico import Politico

politico = Politico()

v2_vote = Blueprint('v2_vote', __name__, url_prefix='/api/v2/votes')

@v2_vote.route("", methods=["POST"])
@login_required
def vote_candidate():
    response = {}
    if request.method == 'POST':
        try:
            vote_data = request.json
            candidate_id = vote_data.get("candidate_id")
            office_id = vote_data.get("office_id")
            voter_id = vote_data.get("voter_id")
            #create vote
            vote = politico.create_vote(candidate_id, office_id, voter_id)
            response["status"] = 201
            response["data"] = vote
            return jsonify(response)
        except InputError as error:
            response["status"] = 400
            response["error"] = error.message
            return jsonify(response), response["status"]




