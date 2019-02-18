from api.v2.database import Database
from api.v2.models.errors import DBError, AuthError


class PoliticalOffice(dict):
    def __init__(self, id, name, office_type):
        self["id"] = id
        self["name"] = name
        self["office_type"] = office_type

    @staticmethod
    def save_office(name, office_type):
        try:
            db = Database.get_connection()
            cur = db.cursor()
            cur.execute(
                "INSERT INTO political_office (name, office_type) VALUES (%s, %s) RETURNING id;",
                (name,
                 office_type))
            insert_id = cur.fetchone()[0]
            db.commit()
            return PoliticalOffice(insert_id, name, office_type)
        except Exception as error:
            print(error)
            cur.execute("ROLLBACK")
            db.commit()
            raise DBError('an error occured when creating political office')

    @staticmethod
    def get_office_by_name(name):
        db = Database.get_connection()
        cur = db.cursor()
        cur.execute("SELECT * FROM political_office where name = %s", (name,))
        office = cur.fetchone()
        if(office is not None):
            office_id = office[0]
            name = office[1]
            office_type = office[2]
            return PoliticalOffice(office_id, name, office_type)
        else:
            return None

    @staticmethod
    def get_office_by_id(office_id):
        db = Database.get_connection()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM political_office where id = %s", (office_id,))
        office = cur.fetchone()
        if(office is not None):
            name = office[1]
            office_type = office[2]
            return PoliticalOffice(office_id, name, office_type)
        else:
            return None

    @staticmethod
    def update_political_office(office_id, name):
        try:
            office = PoliticalOffice.get_office_by_id(office_id)
            if(office is not None):
                db = Database.get_connection()
                cur = db.cursor()
                cur.execute(
                    "UPDATE political_office SET name = %s where id = %s", (name, office_id))
                db.commit()
                office["name"] = name
                return office
            else:
                return None
        except Exception as error:
            print(error)
            cur.execute("ROLLBACK")
            db.commit()
            raise DBError('an error occured when updating political office')

    @staticmethod
    def delete_political_office(office_id):
        try:
            office = PoliticalOffice.get_office_by_id(office_id)
            if(office is not None):
                db = Database.get_connection()
                cur = db.cursor()
                cur.execute(
                    "DELETE FROM political_office WHERE id = %s", (office_id,))
                db.commit()
                return office
            else:
                return None
        except Exception as error:
            print(error)
            cur.execute("ROLLBACK")
            db.commit()
            raise DBError('an error occured when deleting political office')

    @staticmethod
    def get_political_offices():
        try:
            db = Database.get_connection()
            cur = db.cursor()
            cur.execute("SELECT * FROM political_office")
            offices = []
            for office in cur:
                office_id = office[0]
                name = office[1]
                office_type = office[2]
                offices.append(PoliticalOffice(office_id, name, office_type))
            return offices
        except Exception as error:
            cur.execute("ROLLBACK")
            db.commit()
            raise DBError('an error occured when getting political offices')
