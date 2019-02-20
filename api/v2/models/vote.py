from api.v2.database import Database
from api.v2.models.errors import DBError, AuthError, InputError
import psycopg2

class Vote(dict):
    def __init__(self, candidate_id, office_id, voter_id):
        self["candidate_id"] = candidate_id
        self["voter_id"] = voter_id
        self["office_id"] = office_id
    
    @staticmethod
    def get_vote_by_id(voter_id):
        db = Database.get_connection()
        cur = db.cursor()
        cur.execute("SELECT * FROM votes where voter_id = %s", (voter_id,))
        vote = cur.fetchone()
        if(vote is not None):
            candidate_id = vote[0]
            voter_id = vote[1]
            office_id = vote[2]
            return Vote(candidate_id, voter_id, office_id)
        else:
            return None


    @staticmethod
    def save_votes(office_id, candidate_id, voter_id):
        try:
            db = Database.get_connection()
            cur = db.cursor()
            cur.execute(
                "INSERT INTO votes (candidate_id, office_id, voter_id) VALUES (%s, %s, %s)",
                (candidate_id,
                office_id,
                voter_id))
            db.commit()
            return Vote(voter_id, office_id, candidate_id)
        except psycopg2.IntegrityError as error:
            print(error)
            raise InputError('This voter has voted for this office already')
        except Exception as error:
            print(error)
            cur.execute("ROLLBACK")
            db.commit()
            raise DBError('an error occured when creating a vote')