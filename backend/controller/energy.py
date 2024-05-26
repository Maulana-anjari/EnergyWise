from model import energy
import pandas as pd
import pickle
import os
import pmdarima as pm
from datetime import datetime
from fpdf import FPDF
import calendar 

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
MODEL_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "EnergyWise", "arima_models"))

def load_latest_arima_model():
    models = os.listdir(MODEL_DIRECTORY)
    if models:
        latest_model = max(models)
        with open(os.path.join(MODEL_DIRECTORY, latest_model), "rb") as f:
            return pickle.load(f)
    else:
        return None
    
def save_arima_model(model, timestamp):
    model_name = f"arima_model_{timestamp}.pkl"
    with open(os.path.join(MODEL_DIRECTORY, model_name), "wb") as f:
        pickle.dump(model, f)

def ARIMA_model():
    try:
        model = load_latest_arima_model()
        
        energy_data = energy.get_total_energy_by_hour() 
        if not energy_data: 
            return "Data Not Available"
        
        df = pd.DataFrame(energy_data, columns=['timestamp', 'energy_consumption'])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        
        if model is None:
            model = pm.auto_arima(df['energy_consumption'], trace=True, error_action='ignore', suppress_warnings=True)
        fitted_model = model.fit(df['energy_consumption'])

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        save_arima_model(fitted_model, timestamp=timestamp)

        forecast = fitted_model.predict(n_periods=24)
        return forecast
    except Exception as e:
        return str(e)
    
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