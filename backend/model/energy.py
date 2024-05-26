from model import db_params
import psycopg2

def get_energy(month=None, device_id=None):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    print(device_id)

    if month is None and device_id is None:
        query = """
            SELECT 
                eud.data_id,
                eud.device_id,
                eud.timestamp,
                eud.energy_consumption,
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
            ORDER BY
                eud.timestamp"""
        params = None
    elif device_id is None:
        query = """
            SELECT 
                eud.data_id,
                eud.device_id,
                eud.timestamp,
                eud.energy_consumption,
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
        params = (month,)
    elif  month is None:
        query = """        
        SELECT 
            eud.data_id,
            eud.device_id,
            eud.timestamp,
            eud.energy_consumption,
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
            eud.device_id = %s
        ORDER BY
            eud.timestamp"""
        params = (device_id,)
    else:
        query = """        
        SELECT 
            eud.data_id,
            eud.device_id,
            eud.timestamp,
            eud.energy_consumption,
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
            eud.device_id = %s
            AND EXTRACT(MONTH FROM eud.timestamp) = %s
        ORDER BY
            eud.timestamp"""
        params = (device_id, month)

    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.commit()
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()
    
    return result

def get_total_energy():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    query = """
        SELECT 
            DATE_TRUNC('day', eud.timestamp) AS day,
            SUM(eud.energy_consumption) AS total_energy_consumption
        FROM
            public.energy_usage_data eud
        JOIN
            public.iot_device id ON eud.device_id = id.device_id
        JOIN
            public.room r ON id.room_id = r.room_id
        GROUP BY
            day
        ORDER BY
            day;
    """
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()
    return result

def get_total_energy_by_month(month):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    query = """
        SELECT 
            DATE_TRUNC('day', eud.timestamp) AS day,
            SUM(eud.energy_consumption) AS total_energy_consumption
        FROM
            public.energy_usage_data eud
        JOIN
            public.iot_device id ON eud.device_id = id.device_id
        JOIN
            public.room r ON id.room_id = r.room_id
        WHERE
            EXTRACT(MONTH FROM eud.timestamp) = %s
        GROUP BY
            day
        ORDER BY
            day;
        """
    params = (month, )
    
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.commit()
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()
    return result


def get_total_energy_by_hour():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    query ="""
        SELECT 
            DATE_TRUNC('hour', eud.timestamp) AS timestamp_hour,
            SUM(eud.energy_consumption) AS total_energy_consumption
        FROM
            public.energy_usage_data eud
        JOIN
            public.iot_device id ON eud.device_id = id.device_id
        JOIN
            public.room r ON id.room_id = r.room_id
        GROUP BY
            timestamp_hour
        ORDER BY
            timestamp_hour;
    """

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        conn.commit()
    except Exception as e:
        return str(e)
    finally:
        cursor.close()
        conn.close()
    return result