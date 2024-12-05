from flask import Flask, render_template, request, jsonify, redirect
import pymysql
import os
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)

static_folder_path = os.path.join(app.root_path, 'static/images')

# MariaDB 데이터베이스 연결 설정
app.config['MYSQL_HOST'] = 'localhost'  # MariaDB 호스트
app.config['MYSQL_USER'] = 'root'  # MariaDB 사용자
app.config['MYSQL_PASSWORD'] = 'ubuntu'  # MariaDB 비밀번호
app.config['MYSQL_DB'] = 'raspi_db'  # 사용할 데이터베이스

# MySQL 연결 객체 생성
mysql = MySQL(app)

socketio = SocketIO(app, cors_allowed_origins="*")  # CORS 설정
@socketio.on('message')
def handle_message(data):
    print('Received message from Python client:', data)
    # 받은 메시지를 웹 클라이언트로 전달 (경고창으로 띄우도록)

    if data in ["sonic","pwd_comp_err"]:
        emit('show_alert', data, broadcast=True)

    elif data in ["openDoor","lockDoor"]:
        emit('doorControl', data, broadcast=True)

    elif data in ["bell_agree","bell_disagree"]:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE user_info SET name = %s WHERE name = %s", (data, 'bell'))
        mysql.connection.commit()

        cur.execute("SELECT * FROM user_info")
        results = cur.fetchall()
        
        for row in results:
            print(row)

        cur.close()

    else:
        #cur = mysql.connection.cursor()
        #cur.execute("SELECT * FROM user_info WHERE name = 'bell' and address = "+data)
        #result = cur.fetchone()  # 한 튜플만 가져오기

        #if result:
        #    img_input = result[4]

        #cur.close()
        
        emit('bell_pushed', {
        "msg": "누군가 초인종을 눌렀습니다.",
        "img": data
    }, broadcast=True)

#@socketio.on('send_command')
#def send_command(data):
#    print(f'명령 수신: {data}')



@app.route('/')
def index():
    # 조회된 이미지 파일명과 업로드 시간 전달
    return render_template('main_page.html')

@app.route('/auth')
def auth():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_info where name = 'pwd_comp_corr' or name = 'bell_agree'")
    images = cur.fetchall()  # 쿼리 결과를 튜플 리스트로 반환
    cur.close()
    
    # 조회된 이미지 파일명과 업로드 시간 전달
    return render_template('main_page.html', images=images)

@app.route('/dis')
def dis():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_info where name = 'pwd_comp_err' or name = 'bell_disagree'")
    images = cur.fetchall()  # 쿼리 결과를 튜플 리스트로 반환
    cur.close()
    
    # 조회된 이미지 파일명과 업로드 시간 전달
    return render_template('main_page.html', images=images)

@app.route('/del', methods=['GET'])
def delete():
    # GET 매개변수 가져오기
    name_d = request.args.get('name_d')
    address_d = request.args.get('address_d')
    
    file_path = os.path.join(static_folder_path, address_d+".jpg")
    
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        return jsonify({"error": "File not found"}), 404

    cur = mysql.connection.cursor()
    cur.execute("delete from user_info where address = %s",(address_d,))
    mysql.connection.commit()
    cur.close()

    if name_d in ["pwd_comp_corr","bell_agree"]:
        return redirect('/auth')

    if name_d in ["pwd_comp_err","bell_disagree"]:
        return redirect('/dis')

    # JSON 응답 반환
    return jsonify({'message': response_message})

@app.route('/pwd_change', methods=['POST'])
def handle_password():
    data = request.get_json()
    password = data.get('password')

    with open("passwd_rpi", "w") as file:
        file.write(password)

    return jsonify({"message": password})
    
if __name__ == '__main__':
    #app.run(debug=True, port=80, host='0.0.0.0')
    socketio.run(app, debug=True, host='0.0.0.0', port=80)