import obd
import sys
import time
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='Reads data from OBD 2')

parser.add_argument('--obd_device', metavar='d', type=str, required=True,
                   help='OBD device file path')
parser.add_argument('--sleep_time', metavar='s', type=float, required=True,
                   help='Sleep time after each data fetch operation')
parser.add_argument('--nb_data_fetch', metavar='n', type=int, required=True,
                   help='The number of data fetch operations')
parser.add_argument('--vehicle_name', metavar='v', type=str, required=True,
                   help='Specifies the vehicle name')
parser.add_argument('--vehicle_matricule', metavar='m', type=str, required=True,
                   help='Specifies the vehicle name')

args = parser.parse_args()

sleep_time, nb_data_fetch, obd_device, vehicle_name, vehicle_matricule = args.sleep_time, args.nb_data_fetch, args.obd_device, args.vehicle_name, args.vehicle_matricule

connection = obd.OBD(obd_device) # obd.OBD() if you have OBD2 device connected
 
mission_time = str(datetime.now())

lines = []

lines.append("MISSION_INFO")
lines.append(' || '.join(map(str, ["MISSION_START", mission_time] ) ))
lines.append(' || '.join(map(str, ["MISSION_END", mission_time] ) ))
lines.append(' || '.join(map(str, ["VEHICLE_NAME", vehicle_name] ) ))
lines.append(' || '.join(map(str, ["VEHICLE_MATRICULE", vehicle_matricule] ) ))

commands = [
    obd.commands.FUEL_STATUS, 
    obd.commands.ENGINE_LOAD, 
    obd.commands.COOLANT_TEMP, 
    obd.commands.INTAKE_PRESSURE, 
    obd.commands.RPM, 
    obd.commands.SPEED, 
    obd.commands.INTAKE_TEMP, 
    obd.commands.MAF, 
    obd.commands.RUN_TIME, 
    obd.commands.DISTANCE_W_MIL, 
    obd.commands.BAROMETRIC_PRESSURE, 
    obd.commands.FUEL_TYPE, 
    # obd.commands.FUEL_PRESSURE, 
    # obd.commands.FUEL_LEVEL, 
    # obd.commands.FUEL_RATE
]

for i in range(nb_data_fetch):
    lines.append("DATA")
    lines.append(' || '.join(map(str, ["RECORD_TIME", datetime.now()] ) ))
    for cmd in commands:
        response = connection.query(cmd)
        cmd_pid, description = [i.strip() for i in str(cmd).split(':')]
        lines.append( ' || '.join( map(str, [cmd_pid, description, response.value] ) ) ) 
    time.sleep(sleep_time)

for i in lines:
    print(i)