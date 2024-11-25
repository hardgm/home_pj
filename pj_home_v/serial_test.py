import serial
import time

ser = serial.Serial('/dev/serial0',9600,timeout=1)
time.sleep(2)

message = "from RPI!"
ser.write(message.encode('ascii'))

with open("passwd_rpi", "r") as file:
    stored_passwd = file.read()

while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('ascii',errors='replace').strip()
        print(f"Received: {data}")

        if data == "pwd_comp":
            message = stored_passwd
            ser.write(message.encode('ascii'))
            data = "wait"

        if data == "pwd_comp_err":
            data = "wait"
        
        if data == "sonic":
            data = "wait"

        if data == "bell":
            data = "wait"

ser.close()