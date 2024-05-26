from model import  user
import bcrypt

def register(username, email, password):
    try:
        get_user = user.get_user(email)
        if get_user:
            return "User Already Registered"
        else:
            insert_user = user.insert_user(username, email, password)
            return insert_user
    except Exception as e:
        return str(e)
    
def login(username_or_email, password):
    try: 
        get_user = user.get_user(username_or_email)
        if get_user:
            stored_password = get_user[-1]
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return "User logged in"
            else:
                return "Password Incorrect"
        else:
            return "User not Logged In"
    except Exception as e:
        return str(e)

