import psycopg2
import random
from datetime import datetime, timedelta

from dotenv import load_dotenv
import os

load_dotenv()

db_params = {
    'host': os.getenv('DB_HOST'),
    'database':  os.getenv('DB_NAME'),
    'user':  os.getenv('DB_USER'),
    'password':  os.getenv('DB_PASSWORD'),
    'port':  os.getenv('DB_PORT'),
}

def insert_dummy_data():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # users = [
    #     ('dutaramadhan', 'duta2711@gmail.com', 'admin', 'duta2711'),
    #     ('user2', 'user2@example.com', 'user', 'user2'),
    #     ('user3', 'user3@example.com', 'user', 'user3')
    # ]
    # cursor.executemany("""
    #     INSERT INTO public.users (username, email, role, password)
    #     VALUES (%s, %s, %s, %s)
    #     """, users)

    # rooms = [
    #     ('Conference Room', 1, '100m2'),
    #     ('Office 101', 1, '20m2'),
    #     ('Lobby', 0, '50m2')
    # ]
    # cursor.executemany("""
    #     INSERT INTO public.room (room_name, floor, area)
    #     VALUES (%s, %s, %s)
    # """, rooms)


    # iot_devices = [
    #     (1, 1, 'energy_meter', 'active'),
    #     (2, 1, 'energy_meter', 'active'),
    #     (3, 2, 'energy_meter', 'active')
    # ]
    # cursor.executemany("""
    #     INSERT INTO public.iot_device (device_id, room_id, device_type, status)
    #     VALUES (%s, %s, %s, %s)
    # """, iot_devices)

    start_time = datetime.now() - timedelta(days=130)
    energy_usage_data = []

    for device_id in range(1, 4):
        current_time = start_time
        while current_time < datetime.now():
            energy_consumption = round(random.uniform(1, 20), 2)
            energy_usage_data.append((device_id, current_time, energy_consumption))
            current_time += timedelta(minutes=10)

    cursor.executemany("""
        INSERT INTO public.energy_usage_data (device_id, "timestamp", energy_consumption)
        VALUES (%s, %s, %s)
    """, energy_usage_data)

    conn.commit()
    print("Success")
    cursor.close()
    conn.close

insert_dummy_data()