import serial
import time

ser = serial.Serial('/dev/serial0',9600,timeout=1)
time.sleep(2)

message = "from RPI!"
ser.write(message.encode('ascii'))

while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('ascii',errors='replace').strip()
        print(f"Received: {data}")
    #if data == "exit":
    #    break

ser.close()
