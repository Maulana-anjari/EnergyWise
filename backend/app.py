from flask import Flask, request, jsonify
import os
from controller import user

app = Flask(__name__)

@app.route('/')
def info():
    return 'Server is Running on port ' + os.getenv('APP_PORT')

@app.route('/api/users/register', methods=['POST'])
def register():
    data = request.get_json()

    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Username, Email and Password are Required'})

    username = data['username']
    email = data['email']
    password = data['password']

    try:
        response = user.register(username, email, password)
        return jsonify({'message': response})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()

    if 'username_or_email' not in data or 'password' not in data:
        return jsonify({'error': 'Fill the Field Correctly'})
    
    username_or_email = data['username_or_email']
    password = data['password']

    try:
        response = user.login(username_or_email, password)
        return jsonify({'message': response})
    except Exception as e:
        return jsonify({'error': str(e)})
        
if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('APP_PORT'))