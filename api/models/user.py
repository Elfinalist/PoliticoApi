import jwt
from api.database import Database
from api.models.errors import DBError

secret = "Ypw,U$f]]Q:lXxlADxqVso6}8p+Qey"

class User(dict):
    def __init__(self, name, email, password):
        self["name"] = name
        self["email"] = email
        self["password"] = password
        self.save_user()

    def save_user(self):
        try:
            db = Database.get_connection()
            cur = db.cursor()
            cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s) RETURNING id;", 
                (self.get("name"), self.get("email"), self.get("password"))
            )
            insert_id = cur.fetchone()[0]
            self["id"] = insert_id
            db.commit()
        except Exception as error:
            print(error)
            cur.execute("ROLLBACK")
            db.commit()
            raise DBError('an error occured when creating user')
    
    def create_token(self):
        token =  jwt.encode({'id': self["id"]}, secret, algorithm ='HS256')
        return token.decode('utf-8')

    @staticmethod
    def get_user_by_id(user_id):
        pass
    
    @staticmethod
    def get_user_by_email(email):
        pass