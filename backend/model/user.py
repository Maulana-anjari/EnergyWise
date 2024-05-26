from model import db_params
import psycopg2
import bcrypt

def insert_user(username, email, password): 
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    col_name = "username, email, password"
    table_name = "users"

    query = "INSERT INTO {} ({}) VALUES (%s, %s, %s)"
    query = query.format(table_name, col_name)
    try:
        cursor.execute(query, (username, email, hashed_password))
        conn.commit()
        return "Successfully Registered"
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        cursor.close()
        conn.close()

def get_user(username_or_email):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    table_name = "users"

    query = "SELECT * FROM {} WHERE (username = %s OR email = %s)"
    query = query.format(table_name)

    try:
        cursor.execute(query, (username_or_email, username_or_email))
        user = cursor.fetchone()
        conn.commit()
        return user
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()