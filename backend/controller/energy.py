from model import energy

def monitor_energy_usage_month(month):
    try:
        energy_usage = energy.get_energy_by_month(month)
        if energy_usage:
            return energy_usage
        else:
            return "Data not Available"
    except Exception as e:
        return str(e)