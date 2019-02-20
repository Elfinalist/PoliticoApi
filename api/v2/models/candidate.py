from api.v2.database import Database
from api.v2.models.errors import DBError, AuthError, InputError
import psycopg2

class Candidate(dict):
    def __init__(self, user_id, office_id):
        self["user_id"] = user_id
        self["office_id"] = office_id

    @staticmethod
    def get_candidate_by_ID(candidate_id):
        db = Database.get_connection()
        cur = db.cursor()
        cur.execute("SELECT * FROM candidates where id = %s", (candidate_id,))
        candidate = cur.fetchone()
        if(candidate is not None):
            user_id = candidate[0]
            office_id = candidate[1]
            return Candidate(office_id, user_id)
        else:
            return None

    @staticmethod
    def save_candidate(user_id, office_id):
        try:
            db = Database.get_connection()
            cur = db.cursor()
            cur.execute(
                "INSERT INTO candidates (office_id, user_id) VALUES (%s, %s);",
                (office_id,
                user_id,))
            db.commit()
            return Candidate(office_id, user_id)
        except psycopg2.IntegrityError as error:
            print(error)
            raise InputError('This candidate has been registered for this office already')
        except Exception as error:
            print(error)
            cur.execute("ROLLBACK")
            db.commit()
            raise DBError('an error occured when creating a candidate')