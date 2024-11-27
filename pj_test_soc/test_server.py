import socket

host = '127.0.0.1'
port = 65432

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, port))
print(f"서버가 {host}:{port}에서 대기하고 있습니다...")

try:
    while True:  
            # 클라이언트로부터 데이터 수신
            message, client_address = server_socket.recvfrom(1024)
            message_str = message.decode()
            print(f"클라이언트({client_address})로부터 메시지 수신: {message_str}")
            name = "test"
            server_socket.sendto(name.encode(),client_address)
except Exception as e:
    print(f"에러 발생: {e}")
finally:
    server_socket.close()