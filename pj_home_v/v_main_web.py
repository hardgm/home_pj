from flask import Flask, render_template
import pymysql
from flask_mysqldb import MySQL

app = Flask(__name__)

# MariaDB 데이터베이스 연결 설정
app.config['MYSQL_HOST'] = 'localhost'  # MariaDB 호스트
app.config['MYSQL_USER'] = 'root'  # MariaDB 사용자
app.config['MYSQL_PASSWORD'] = 'ubuntu'  # MariaDB 비밀번호
app.config['MYSQL_DB'] = 'raspi_db'  # 사용할 데이터베이스

# MySQL 연결 객체 생성
mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_info")
    images = cur.fetchall()  # 쿼리 결과를 튜플 리스트로 반환
    cur.close()
    
    # 조회된 이미지 파일명과 업로드 시간 전달
    return render_template('img_db_test.html', images=images)

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')