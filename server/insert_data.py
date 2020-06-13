import argparse
import mysql.connector
from mysql.connector import MySQLConnection, Error
# from python_mysql_dbconfig import read_db_config

conn = None

def read_variable(file_lines, i):
    pid, descr, value = file_lines[i].split(' || ')
    return {
        "pid": pid,
        "description": descr,
        "value": value
    }

def read_data_record(file_lines, i):
    assert(file_lines[i] == 'DATA')
    # time
    _, record_time = file_lines[i + 1].split(' || ')
    i += 2
    variables = []
    while i < len(file_lines) and file_lines[i] != 'DATA':
        variables.append(read_variable(file_lines, i))
        i += 1
    return ({"time":record_time, "variables": variables }, i)

def read_mission(file_lines, i = 0):
    assert(file_lines[i].strip() == "MISSION_INFO")
    _, mission_start = file_lines[i + 1].split(' || ')
    _, mission_end = file_lines[i + 2].split(' || ')
    _, vehicle_name = file_lines[i + 3].split(' || ')
    _, vehicle_matricule = file_lines[i + 4].strip().split(' || ')
    i += 5
    data_records = []
    while i < len(file_lines):
        data_record, j = read_data_record(file_lines, i)
        data_records.append(data_record)
        i = j
    mission = {
        "mission_start": mission_start, 
        "mission_end": mission_end,
        "vehicle_name": vehicle_name,
        "vehicle_matricule": vehicle_matricule,
        "data_records": data_records
    }
    return mission

def parse_source_file(source_file):
    mission = []
    with open(source_file, 'r') as f:
        file_lines = [i.strip() for i in f.readlines()]
        mission = read_mission(file_lines)
    return mission

def register_vehicle(vehicle_name, vehicle_matricule):
    global conn
    try:
        cursor = conn.cursor()
        args = (vehicle_name, vehicle_matricule)
        cursor.execute("SELECT id FROM vehicles WHERE name=%s AND matricule=%s", args)
        rows = cursor.fetchall()
        if cursor.rowcount != 0:
            for r in rows:
                return int(r[0])
        query = "INSERT INTO vehicles(name, matricule) VALUES(%s, %s)"
        cursor = conn.cursor()
        cursor.execute(query, args)
        vehicle_id = cursor.lastrowid
        conn.commit()
        return vehicle_id
    except Error as e:
        print(e)
        return None

def register_mission(mission_start, mission_end, vehicle_id):
    global conn
    try:
        cursor = conn.cursor()
        args = (mission_start, mission_end, vehicle_id)
        query = "INSERT INTO missions(start, end, vehicle_id) VALUES(%s, %s, %s)"
        cursor = conn.cursor()
        cursor.execute(query, args)
        ret = cursor.lastrowid
        conn.commit()
        return ret
    except Error as e:
        print(e)
        return None

def register_data_record(record_time, vehicle_id, mission_id):
    global conn
    try:
        cursor = conn.cursor()
        args = (record_time, vehicle_id, mission_id)
        query = "INSERT INTO data_records(record_time, vehicle_id, mission_id) VALUES(%s, %s, %s)"
        cursor = conn.cursor()
        cursor.execute(query, args)
        ret = cursor.lastrowid
        conn.commit()
        return ret
    except Error as e:
        print(e)
        return None

def register_variable(record_id, pid_code, description, value):
    global conn
    try:
        cursor = conn.cursor()
        args = (record_id, pid_code, description, value)
        # cursor.execute("SELECT * FROM missions WHERE start=%s AND end=%s AND vehicle_id=%s", args)
        # rows = cursor.fetchall()
        # if cursor.rowcount != 0:
        #     return
        query = "INSERT INTO variables(record_id, pid_code, description, value) VALUES(%s, %s, %s, %s)"
        cursor = conn.cursor()
        cursor.execute(query, args)
        ret = cursor.lastrowid
        conn.commit()
        return ret
    except Error as e:
        print(e)
        return None

USER = 'user'
PASSWORD = '1475369'
SERVER_ADDRESS = 'localhost'
DATABASE = 'station_db'

parser = argparse.ArgumentParser(description='Inserts data into the database')
parser.add_argument('--source_file', metavar='f', type=str, required=True,
                   help='The file used to insert mission data into the database')

args = parser.parse_args()
source_file = args.source_file

def connect():
    """ Connect to MySQL database """
    global conn
    try:
        conn = mysql.connector.connect(host=SERVER_ADDRESS,
                                       database=DATABASE,
                                       user=USER,
                                       password=PASSWORD)
        if conn.is_connected():
            mission = parse_source_file(source_file)
            vehicle_id = register_vehicle(mission['vehicle_name'], mission['vehicle_matricule'])
            mission_id = register_mission(mission["mission_start"], mission["mission_end"], vehicle_id)
            for data_record in mission["data_records"]:
                data_record_id = register_data_record(data_record["time"], vehicle_id, mission_id)
                for variable in data_record["variables"]:
                    register_variable(data_record_id, variable["pid"], variable["description"], variable["value"])
            print("[+] Data inserted into the database successfully")
    except Error as e:
        print(e)
        print(e.msg)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == '__main__':
    connect()
