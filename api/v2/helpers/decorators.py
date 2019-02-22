import jwt, os
from functools import wraps
from flask import g, jsonify, request
from api.v2.models.user import User

JWT_PASS = 'Ypw,U$f]]Q:lXxlADxqVso6}8p+Qey'
JWT_ALGORITHM = 'HS256'

def get_user_id(token):
   user = jwt.decode(token, JWT_PASS, JWT_ALGORITHM)
   g.user_id = user.get('user_id')
   return ['user_id']

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Please login to access this route'}), 401
        try:
            user = get_user_id(token)
        except jwt.DecodeError:
            return jsonify({'message': 'invalid token'}), 401
        g.user = user
        return func(*args, **kwargs)
    return wrapper

def get_user_role():
    user = User.get_user_by_id(g.user_id)
    print("this is it", g.user_id)
    if user is not None:
        is_admin = user.get('is_admin')
        print(user)
        print(is_admin)
        return is_admin

def is_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        has_admin_rights = get_user_role()
        print(has_admin_rights)
        if not has_admin_rights:
            return jsonify({'message': 'You do not have access to this route'}), 401                
        return func(*args, **kwargs)
    return wrapper

