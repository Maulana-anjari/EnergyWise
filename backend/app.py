from flask import Flask, request, jsonify
import os
from controller import user, energy

app = Flask(__name__)

@app.route('/')
def info():
    return 'Server is Running on port ' + os.getenv('APP_PORT')

#USER SECTION
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


#ENERGY SECTION
@app.route('/api/energy/usage', methods=['GET'])
def get_energy_usage():
    type = request.args.get('type')
    
    if type == 'all':
        return get_all_energy_usage()
    elif type == 'month':
        month = request.args.get('month')
        return get_energy_usage_month(month)
    elif type == 'device':
        device_id = request.args.get('device_id')
        return get_energy_usage_device(device_id)
    elif type == 'month and device':
        month = request.args.get('month')
        device_id = request.args.get('device_id')
        return get_energy_usage_month_and_device(month, device_id)
    else:
        return jsonify({'error': 'Invalid request type'})

def get_all_energy_usage():    
    try: 
        energy_usage = energy.monitor_all_energy_usage()
        return jsonify({'energy_usage': format_energy_usage(energy_usage)})
    except Exception as e:
        return jsonify({'error': str(e)})

def get_energy_usage_month(month):    
    if not month:
        return jsonify({'error': 'Month Parameter is Required'})
    try: 
        energy_usage_month = energy.monitor_energy_usage_by_month(month)
        return jsonify({'energy_usage_month': format_energy_usage(energy_usage_month)})
    except Exception as e:
        return jsonify({'error': str(e)})

def get_energy_usage_device(device_id):    
    if not device_id:
        return jsonify({'error': 'Device ID Parameter is Required'})
    try: 
        energy_usage_device = energy.monitor_energy_usage_by_device_id(device_id)
        return jsonify({'energy_usage_device': format_energy_usage(energy_usage_device)})
    except Exception as e:
        return jsonify({'error': str(e)})

def get_energy_usage_month_and_device(month, device_id):    
    if not month and device_id:
        return jsonify({'error': 'Device ID and Month Parameter is Required'})
    try: 
        energy_usage_month_and_device = energy.monitor_energy_usage_by_month_and_device_id(month, device_id)
        return jsonify({'energy_usage_device': format_energy_usage(energy_usage_month_and_device)})
    except Exception as e:
        return jsonify({'error': str(e)})

def format_energy_usage(energy_usage):
    response = []
    for row in energy_usage:
        response.append({
            "data_id": row[0],
            "device_id": row[1],
            "timestamp": row[2].strftime('%d %m %Y %H:%M:%S GMT'),
            "energy_consumption": row[3],
            "room_id": row[4],
            "device_type": row[5],
            "status": row[6],
            "room_name": row[7],
            "floor": row[8],
            "area": row[9]
        })
    return response

@app.route('/api/energy/usage/total', methods=['GET'])
def get_total_energy_usage():
    try:
        month = request.args.get('month')
        total_energy_usage = None

        if month:
            total_energy_usage = energy.monitor_total_energy_usage_by_month(month)
        else:
            total_energy_usage = energy.monitor_total_energy_usage()
        
        response = []
        for row in total_energy_usage:
            response.append({
                "timestamp": row[0].strftime('%d %m %Y'),
                "energy_consumption": row[1]
            })
        return jsonify({"total_energy_usage": response})
    except Exception as e:
        return jsonify(str(e))

    

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('APP_PORT'))