from model import db_params
import psycopg2

def get_energy_by_month(month):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    query = """
        SELECT 
            eud.data_id,
            eud.device_id,
            eud.timestamp,
            eud.energy_comsumption,
            id.room_id,
            id.device_type,
            id.status,
            r.room_name,
            r.floor,
            r.area
        FROM
            public.energy_usage_data eud
        JOIN
            public.iot_device id ON eud.device_id = id.device_id
        JOIN
            public.room r ON id.room_id = r.room_id
        WHERE
            EXTRACT(MONTH FROM eud.timestamp) = %s
        ORDER BY
            eud.timestamp"""
    try:
        cursor.execute(query, (month))
        result = cursor.fetchall()
    except Exception as e:
        return str(e)
    finally: 
        cursor.close()
        conn.close()
        return result   