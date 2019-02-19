import jwt
from api.v2.database import Database
from api.v2.models.errors import DBError, AuthError

secret = "Ypw,U$f]]Q:lXxlADxqVso6}8p+Qey"


class User(dict):
    def __init__(self, user_id, name, email, password, is_admin):
        self["id"] = user_id
        self["name"] = name
        self["email"] = email
        self["password"] = password
        self["is_admin"] = is_admin

    @staticmethod
    def save_user(name, email, password, is_admin = False):
        try:
            db = Database.get_connection()
            cur = db.cursor()
            cur.execute(
                "INSERT INTO users (name, email, password, is_admin) VALUES (%s, %s, %s, %s) RETURNING id;",
                (name,
                 email,
                 password,
                 is_admin))
            insert_id = cur.fetchone()[0]
            db.commit()
            return User(insert_id, name, email, password, is_admin)
        except Exception as error:
            cur.execute("ROLLBACK")
            db.commit()
            raise DBError('an error occured when creating user')

    def create_token(self):
        token = jwt.encode({'user_id': self["id"]}, secret, algorithm='HS256')
        return token.decode('utf-8')

    @staticmethod
    def get_user_by_id(user_id):
        db = Database.get_connection()
        cur = db.cursor()
        cur.execute("SELECT name, email, password, is_admin FROM users where id = %s", (user_id,))
        user = cur.fetchone()
        if(user is not None):
            name = user[0]
            email = user[1]
            password = user[2]
            is_admin = user[3]
            return User(user_id, name, email, password, is_admin)
        else:
            return None

    @staticmethod
    def get_user_by_email(email):
        db = Database.get_connection()
        cur = db.cursor()
        cur.execute("SELECT * FROM users where email = %s", (email,))
        user = cur.fetchone()
        if(user is not None):
            user_id = user[0]
            name = user[1]
            password = user[3]
            is_admin = user[4]
            return User(user_id, name, email, password, is_admin)
        else:
            return None

    @staticmethod
    def login(email, password):
        user = User.get_user_by_email(email)
        if(user is not None and user.get("password") == password):
            return user

        raise AuthError("invalid email/password")
