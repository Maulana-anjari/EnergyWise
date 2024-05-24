import psycopg2
from config import db_params
import random
from datetime import datetime, timedelta

conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

users = [
    ('dutaramadhan', 'duta2711@gmail.com', 'admin', 'duta2711'),
    ('user2', 'user2@example.com', 'user', 'user2'),
    ('user3', 'user3@example.com', 'user', 'user3')
]
cursor.executemany("""
    INSERT INTO public.users (username, email, role, password)
    VALUES (%s, %s, %s, %s)
    """, users)

# rooms = [
#     ('Conference Room', 1, '100m2'),
#     ('Office 101', 1, '20m2'),
#     ('Lobby', 0, '50m2')
# ]
# cursor.executemany("""
#     INSERT INTO public.room (room_name, floor, area)
#     VALUES (%s, %s, %s)
# """, rooms)


# Insert dummy data into the "iot_device" table
# iot_devices = [
#     (1, 1, 'energy_meter', 'active'),
#     (2, 1, 'energy_meter', 'active'),
#     (3, 2, 'energy_meter', 'active')
# ]
# cursor.executemany("""
#     INSERT INTO public.iot_device (device_id ,room_id, device_type, status)
#     VALUES (%s, %s, %s, %s)
# """, iot_devices)

# def insert_dummy_data():


conn.commit()

cursor.close()
conn.close