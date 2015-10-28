import serial
import os
from Adafruit_IO import Client
import credentials

ser = serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=4800,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=1)

print("connected to: " + ser.portstr)

aio = Client(credentials.ADAFRUIT_IO_KEY)

def degrees_to_decimal(data, hemisphere):
    try:
        decimalPointPosition = data.index('.')
        degrees = float(data[:decimalPointPosition-2])
        minutes = float(data[decimalPointPosition-2:])/60
        output = degrees + minutes
        if hemisphere is 'N' or hemisphere is 'E':
            return output
        if hemisphere is 'S' or hemisphere is 'W':
            return -output
    except:
        return ""

def parse_GPRMC(data):
    data = data.split(',')
    dict = {
            'fix_time': data[1],
            'validity': data[2],
            'latitude': data[3],
            'latitude_hemisphere' : data[4],
            'longitude' : data[5],
            'longitude_hemisphere' : data[6],
            'speed': data[7],
            'true_course': data[8],
            'fix_date': data[9],
            'variation': data[10],
            'variation_e_w' : data[11],
            'checksum' : data[12]
    }
    dict['decimal_latitude'] = degrees_to_decimal(dict['latitude'], dict['latitude_hemisphere'])
    dict['decimal_longitude'] = degrees_to_decimal(dict['longitude'], dict['longitude_hemisphere'])
    return dict

while True:
    line = ser.readline()
    if "$GPRMC" in line:
        gpsData = parse_GPRMC(line)
        if gpsData['validity'] == "A":
            #os.system('clear')
            #print "Lat: " + gpsData['latitude']+gpsData['latitude_hemisphere']
            #print "Long: " + gpsData['longitude']+gpsData['longitude_hemisphere']
            with open("/home/pi/gps_experimentation/log.txt", "a") as myfile:
                myfile.write(gpsData['fix_date'] + "," + gpsData['fix_time'] + "," + gpsData['latitude'] + "," + gpsData['latitude_hemisphere'] + "," + gpsData['longitude'] + "," + gpsData['longitude_hemisphere'] +"\n")
            with open("/home/pi/gps_experimentation/raw_log.txt", "a") as myfile:
                myfile.write(line)
            payload = {'lat': gpsData['decimal_latitude'],
                        'long': gpsData['decimal_longitude']
            }
            aio.send(payload)

