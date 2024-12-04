from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # CORS 설정

@app.route('/')
def index():
    return render_template('index.html')  # 웹 클라이언트 페이지

@socketio.on('message')
def handle_message(data):
    print('Received message from Python client:', data)
    # 받은 메시지를 웹 클라이언트로 전달 (경고창으로 띄우도록)
    emit('show_alert', data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=80)