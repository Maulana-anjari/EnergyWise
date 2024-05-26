from flask import Flask, request, jsonify, send_file
import os
from controller import user, energy
from datetime import datetime
import pandas as pd

app = Flask(__name__)

@app.route('/')
def info():
    return 'Server is Running on port ' + os.getenv('APP_PORT')

#USER SECTION
@app.route('/api/users/register', methods=['POST'])
def register():
    data = request.get_json()

    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Username, Email, and Password are required'}), 400

    username = data['username']
    email = data['email']
    password = data['password']

    try:
        response, status_code = user.register(username, email, password)
        if status_code == 201:
            return jsonify({'message': response}), status_code
        else:
            return jsonify({'error': response}), status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username_or_email' not in data or 'password' not in data:
        return jsonify({'error': 'Please provide both username/email and password'}), 400

    username_or_email = data['username_or_email']
    password = data['password']

    response, status_code = user.login(username_or_email, password)
    if status_code == 200:
        return jsonify({'message': response}), status_code
    else:
        return jsonify({'error': response}), status_code

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
            "timestamp": row[2].strftime('%d-%m-%Y %H:%M:%S GMT'),
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
                "timestamp": row[0].strftime('%d-%m-%Y'),
                "energy_consumption": row[1]
            })
        return jsonify({"total_energy_usage": response})
    except Exception as e:
        return jsonify(str(e))

# #Forecast Section
@app.route('/api/energy/forecast', methods=['GET'])
def forecast():
    try:
        forecast = energy.ARIMA_model()
        if isinstance(forecast, str):
            return jsonify({'error': forecast})
        
        timestamps = pd.date_range(start=datetime.now(), periods=24, freq='H')
        
        response = []
        for i in range(24):
            response.append({
                "timestamp": timestamps[i].strftime('%Y-%m-%d %H:%M:%S'),
                "energy_consumption": forecast[i]
            })
        return jsonify({"forecast": response})
    except Exception as e:
        return jsonify({'error': str(e)})

#Report Section
@app.route('/api/energy/report', methods=['GET'])
def report():
    try:
        month = request.args.get('month')
        if not month:
            return jsonify({"error": "Month is required"}), 400

        data = energy.get_report(month)
        if data is None:
            return jsonify({"error": "No data found for the specified month"}), 404
        
        pdf_path = energy.create_pdf(data, month)
        if not pdf_path:
            return jsonify({"error": "Failed to create PDF"}), 500

        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('APP_PORT'))