import serial
import socket
import pymysql
import time
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

#@sio.on('show_alert')
#def on_show_alert(data):
#    print(f'Alert received: {data}')

# 서버에 메시지를 전송하는 함수
#def send_message_to_server(message):
#    sio.emit('message', message)

# 서버에 연결
sio.connect('http://127.0.0.1:80/')

host = '127.0.0.1'  # 로컬 호스트
port = 65432        # 포트 번호 (클라이언트가 동일한 포트로 연결)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_and_receive_message(message, host, port):
    client_socket.sendto(message.encode(), (host, port))
    response, server_address = client_socket.recvfrom(1024)
    pic_addr = response.decode()
    print(f"서버로부터 응답: {pic_addr}")
    return pic_addr

try:
    # MariaDB 데이터베이스 연결
    conn = pymysql.connect(
    host='localhost',      # 데이터베이스 호스트
    user='root',   # 사용자 이름
    password='ubuntu', # 비밀번호
    database='raspi_db' # 데이터베이스 이름
    )

    # 커서 객체 생성
    cursor = conn.cursor()

    ser = serial.Serial('/dev/serial0',9600,timeout=1)
    time.sleep(2)
    message = "from RPI!"
    ser.write(message.encode('ascii'))

    @sio.on('doorControl')
    def doorControl(data):
        print(f'received: {data}')
        message = data
        ser.write(message.encode('ascii'))

    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('ascii',errors='replace').strip()
            print(f"Received: {data}")

            if data == "pwd_comp":
                
                with open("passwd_rpi", "r") as file:
                    message = file.read()
                
                ser.write(message.encode('ascii'))
                data = "wait"

            if data == "sonic":
                sio.emit('message', data)
                data = "wait"
            
            if data == "bell":
                response = send_and_receive_message(data, host, port)

                cursor.execute('INSERT INTO user_info (name, address) VALUES (%s,%s)', (data,response))
                conn.commit()

                cursor.execute('SELECT * FROM user_info')
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

                sio.emit('message', response)
                data = "wait"
                

            if data == "pwd_comp_corr":
                response = send_and_receive_message(data, host, port)
                cursor.execute('INSERT INTO user_info (name, address) VALUES (%s,%s)', (data,response))
                conn.commit()

                cursor.execute('SELECT * FROM user_info')
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

                data = "wait"

            if data == "pwd_comp_err":
                sio.emit('message', data)
                response = send_and_receive_message(data, host, port)
                cursor.execute('INSERT INTO user_info (name, address) VALUES (%s,%s)', (data,response))
                conn.commit()

                cursor.execute('SELECT * FROM user_info')
                rows = cursor.fetchall()
                for row in rows:
                    print(row)

                

                data = "wait"

except Exception as e:
    print(f"에러 발생: {e}")

finally:
    ser.close()
    client_socket.close()
    cursor.close()
    conn.close()