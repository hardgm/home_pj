import socket

def start_client():
    # 서버 주소 및 포트 설정
    host = '127.0.0.1'  # 서버 IP (서버와 동일한 컴퓨터에서 실행)
    port = 65432        # 서버에서 사용한 포트 번호

    # 클라이언트 소켓 생성
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # 서버에 연결
        client_socket.connect((host, port))

        while True:
            # 서버로 메시지 전송
            message = input("서버에 보낼 메시지를 입력하세요: ")
            if message.lower() == 'exit':
                break  # 'exit' 입력 시 연결 종료
            client_socket.sendall(message.encode())

            # 서버의 응답 수신
            data = client_socket.recv(1024)
            print(f"서버로부터 응답 수신: {data.decode()}")

if __name__ == "__main__":
    start_client()