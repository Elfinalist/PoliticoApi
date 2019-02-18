from api.v2.database import Database
from api.v2.models.errors import DBError, AuthError


class PoliticalParty(dict):
    def __init__(self, id, name, hq, logo_url):
        self["id"] = id
        self["name"] = name
        self["hq"] = hq
        self["logoUrl"] = logo_url

    @staticmethod
    def save_party(name, hq, logo_url):
        try:
            db = Database.get_connection()
            cur = db.cursor()
            cur.execute(
                "INSERT INTO political_party (name, hq, logo_url) VALUES (%s, %s, %s) RETURNING id;",
                (name,
                 hq,
                 logo_url))
            insert_id = cur.fetchone()[0]
            db.commit()
            return PoliticalParty(insert_id, name, hq, logo_url)
        except Exception as error:
            print(error)
            cur.execute("ROLLBACK")
            db.commit()
            raise DBError('an error occured when creating political party')

    @staticmethod
    def get_party_by_name(name):
        db = Database.get_connection()
        cur = db.cursor()
        cur.execute("SELECT * FROM political_party where name = %s", (name,))
        party = cur.fetchone()
        if(party is not None):
            party_id = party[0]
            name = party[1]
            hq = party[2]
            logo_url = party[3]
            return PoliticalParty(party_id, name, hq, logo_url)
        else:
            return None

    @staticmethod
    def get_party_by_id(party_id):
        db = Database.get_connection()
        cur = db.cursor()
        cur.execute("SELECT * FROM political_party where id = %s", (party_id,))
        party = cur.fetchone()
        if(party is not None):
            name = party[1]
            hq = party[2]
            logo_url = party[3]
            return PoliticalParty(party_id, name, hq, logo_url)
        else:
            return None

    @staticmethod
    def update_political_party(party_id, name):
        try:
            party = PoliticalParty.get_party_by_id(party_id)
            if(party is not None):
                db = Database.get_connection()
                cur = db.cursor()
                cur.execute(
                    "UPDATE political_party SET name = %s where id = %s", (name, party_id))
                db.commit()
                party["name"] = name
                return party
            else:
                return None
        except Exception as error:
            print(error)
            cur.execute("ROLLBACK")
            db.commit()
            raise DBError('an error occured when updating political party')

    @staticmethod
    def delete_political_party(party_id):
        try:
            party = PoliticalParty.get_party_by_id(party_id)
            if(party is not None):
                db = Database.get_connection()
                cur = db.cursor()
                cur.execute(
                    "DELETE FROM political_party WHERE id = %s", (party_id,))
                db.commit()
                return party
            else:
                return None
        except Exception as error:
            print(error)
            cur.execute("ROLLBACK")
            db.commit()
            raise DBError('an error occured when deleting political party')

    @staticmethod
    def get_political_parties():
        try:
            db = Database.get_connection()
            cur = db.cursor()
            cur.execute("SELECT * FROM political_party")
            parties = []
            for party in cur:
                party_id = party[0]
                name = party[1]
                hq = party[2]
                logo_url = party[3]
                parties.append(PoliticalParty(party_id, name, hq, logo_url))
            return parties
        except Exception as error:
            print(error)
            cur.execute("ROLLBACK")
            db.commit()
            raise DBError('an error occured when getting political parties')
