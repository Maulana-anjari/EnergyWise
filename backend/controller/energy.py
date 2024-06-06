from model import energy
import pandas as pd
import pickle
import os
import pmdarima as pm
from datetime import datetime
from fpdf import FPDF
import calendar 
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

def monitor_amount_of_rooms():
    try:
        rooms = energy.get_rooms()
        if rooms:
            return rooms
        else:
            return "Data not Available"
    except Exception as e:
        return str(e)
    
def monitor_amount_of_devices():
    try:
        devices = energy.get_devices()
        if devices:
            return devices
        else:
            return "Data not Available"
    except Exception as e:
        return str(e)
    
def monitor_all_energy_usage():
    try:
        energy_usage = energy.get_energy()
        if energy_usage:
            return energy_usage
        else:
            return "Data not Available"
    except Exception as e:
        return str(e)
    
def monitor_energy_usage_by_month(month):
    try:
        energy_usage = energy.get_energy(month = month)
        if energy_usage:
            return energy_usage
        else:
            return "Data not Available"
    except Exception as e:
        return str(e)

def monitor_energy_usage_by_device_id(device_id):    
    try:
        energy_usage = energy.get_energy(device_id = device_id)
        if energy_usage:
            return energy_usage
        else:
            return "Data not Available"
    except Exception as e:
        return str(e)

def monitor_energy_usage_by_month_and_device_id(month, device_id):
    try: 
        energy_usage = energy.get_energy(month = month, device_id = device_id)
        if energy_usage:
            return energy_usage
        else:
            return "Data Not Available"
    except Exception as e:
        return str(e)
    
def monitor_total_energy_usage():
    try: 
        total_energy_usage = energy.get_total_energy()
        return total_energy_usage if total_energy_usage else "Data Not Available"
    except Exception as e:
        return str(e)
    
def monitor_total_energy_usage_by_month(month):
    try: 
        total_energy_usage = energy.get_total_energy_by_month(month)
        return total_energy_usage if total_energy_usage else "Data Not Available"
    except Exception as e:
        return str(e)

#Forecasting Section
MODEL_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "EnergyWise", "lstm_models"))

def load_latest_lstm_model():
    models = os.listdir(MODEL_DIRECTORY)
    if models:
        latest_model = max(models)
        model = load_model(os.path.join(MODEL_DIRECTORY, latest_model))
        model.compile(optimizer='adam', loss='mean_squared_error')  # Recompile the model
        return model
    else:
        return None

def save_lstm_model(model, timestamp):
    model_name = f"lstm_model_{timestamp}.h5"
    model.save(os.path.join(MODEL_DIRECTORY, model_name))

def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def LSTM_model():
    try:
        model = load_latest_lstm_model()
        
        energy_data = energy.get_total_energy_by_hour() 
        if not energy_data: 
            return "Data Not Available"
        
        df = pd.DataFrame(energy_data, columns=['timestamp', 'energy_consumption'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        dataset = df['energy_consumption'].values.reshape(-1, 1)
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)
        
        X_train = []
        y_train = []
        for i in range(60, len(scaled_data)):
            X_train.append(scaled_data[i-60:i, 0])
            y_train.append(scaled_data[i, 0])
        
        X_train, y_train = np.array(X_train), np.array(y_train)
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        
        if model is None:
            model = create_lstm_model((X_train.shape[1], 1))
        
        model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=2)
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        save_lstm_model(model, timestamp=timestamp)
        
        # Forecasting for the next 24 hours
        inputs = df['energy_consumption'][-60:].values.reshape(-1, 1)
        inputs = scaler.transform(inputs)
        X_test = inputs.reshape(1, inputs.shape[0], 1)
        
        forecast = []
        for _ in range(24):
            prediction = model.predict(X_test)
            forecast.append(prediction[0, 0])
            # Update X_test with the new prediction, ensuring consistent dimensions
            X_test = np.append(X_test[:, 1:, :], np.reshape(prediction, (1, 1, 1)), axis=1)
        
        forecast = scaler.inverse_transform(np.array(forecast).reshape(-1, 1)).flatten().tolist()  # Convert to list of native floats
        
        return forecast, df.index[-1]  # Return the forecast and the last timestamp
    except Exception as e:
        return str(e), None

#Report Section
def get_report(month):
    data = energy.get_total_energy_by_month(month)
    modified_data = []
    for row in data:
        modified_row = list(row)
        modified_row[0] = modified_row[0].strftime('%Y-%m-%d')
        modified_data.append(modified_row)
    df = pd.DataFrame(modified_data, columns=['timestamp', 'energy_consumption'])
    return df

def create_pdf(data, month):
    pdf = FPDF()
    pdf.add_page()

    month_name = calendar.month_name[int(month)]

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Energy Consumption Report for {month_name}", ln=True, align='C')

    pdf.ln(10) 

    table_col_widths = [70, 70]
    table_total_width = sum(table_col_widths)
    page_width = pdf.w - 2 * pdf.l_margin
    start_x = (page_width - table_total_width) / 2 + pdf.l_margin

    pdf.set_x(start_x)

    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(table_col_widths[0], 10, 'Timestamp', border=1, align='C')
    pdf.cell(table_col_widths[1], 10, 'Energy Consumption', border=1, align='C')
    pdf.ln()

    pdf.set_x(start_x)

    pdf.set_font("Arial", size=10)
    for index, row in data.iterrows():
        pdf.cell(table_col_widths[0], 10, str(row['timestamp']), border=1, align='C')
        pdf.cell(table_col_widths[1], 10, str(row['energy_consumption']), border=1, align='C')
        pdf.ln()
        pdf.set_x(start_x)  

    output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "EnergyWise", "Report"))
    pdf_output = os.path.join(output_folder, f"energy_report_{month_name}.pdf")
    pdf.output(pdf_output)
    return pdf_output