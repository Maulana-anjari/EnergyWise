from model import energy

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
