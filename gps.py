import serial

ser = serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=4800,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=1)

print("connected to: " + ser.portstr)

def parse_GPRMC(data):
    data = data.split(',')
    dict = {
            'utc': data[1],
            'validity': data[2],
            'latitude': data[3],
            'latitude_n_s' : data[4],
            'longitude' : data[5],
            'longitude_e_w' : data[6],
            'speed': data[7],
            'true_course': data[8],
            'date_stamp': data[9],
            'variation': data[10],
            'variation_e_w' : data[11],
            'checksum' : data[12]
    }
    return dict

while True:
    line = ser.readline()
    if "$GPRMC" in line:
        gpsData = parse_GPRMC(line)
        if gpsData['validity'] == "A":
            print "Lat: " + gpsData['latitude']+gpsData['latitude_n_s']
            print "Long: " + gpsData['longitude']+gpsData['longitude_e_w']