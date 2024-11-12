import pymysql
from flask import Flask, jsonify

# Flask 애플리케이션 생성
app = Flask(__name__)

# MySQL 연결 설정 (자신의 데이터베이스 정보로 수정)
def get_db_connection():
    connection = pymysql.connect(
        host='localhost',         # MySQL 서버 주소 (로컬이라면 localhost)
        user='root',     # MySQL 사용자명
        password='ubuntu', # MySQL 비밀번호
        db='test',       # 사용할 데이터베이스 이름
        charset='utf8mb4'         # 문자셋 설정
    )
    return connection

# 기본 라우트
@app.route('/')
def home():
    return "Flask와 PyMySQL 연동 테스트!"

# 데이터베이스에서 데이터 조회하는 라우트
@app.route('/get-data')
def get_data():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 예시로 'users' 테이블에서 모든 데이터를 조회
            cursor.execute("SELECT * FROM users;")
            result = cursor.fetchall()  # 모든 결과를 가져옴
            # 결과를 JSON 형식으로 반환
            return jsonify(result)
    except Exception as e:
        return str(e)
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')