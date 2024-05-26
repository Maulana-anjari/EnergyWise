from model import  user
import bcrypt
from flask import jsonify

class UserAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class InvalidPasswordError(Exception):
    pass

def register(username, email, password):
    try:
        get_user = user.get_user(email)
        if get_user:
            raise UserAlreadyExistsError("User already registered")
        
        insert_user = user.insert_user(username, email, password)
        return insert_user, 201
    except UserAlreadyExistsError as e:
        return str(e), 409
    except Exception as e:
        return str(e), 500
    
def login(username_or_email, password):
    try:
        get_user = user.get_user(username_or_email)
        if not get_user:
            raise UserNotFoundError("User not found")
        
        stored_password = get_user[-1]
        if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            raise InvalidPasswordError("Password incorrect")

        return "User logged in", 200
    except UserNotFoundError as e:
        return str(e), 404
    except InvalidPasswordError as e:
        return str(e), 401
    except Exception as e:
        return str(e), 500