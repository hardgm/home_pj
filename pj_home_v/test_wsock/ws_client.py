import socketio

# SocketIO 클라이언트 인스턴스 생성
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
def send_message_to_server(message):
    sio.emit('message', message)

# 서버에 연결
sio.connect('http://127.0.0.1:80/')

# 서버로 메시지 전송
send_message_to_server("Hello from Python client!")

# 무한 루프처럼 유지되도록 이벤트 루프 실행
while True:
    pass  # 다른 코드가 실행되지 않도록 무한 루프를 지속