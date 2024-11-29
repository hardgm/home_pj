import socket
import time

host = '127.0.0.1'  # 로컬 호스트
port = 65432        # 포트 번호 (클라이언트가 동일한 포트로 연결)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 서버로 메시지 전송
try:
        message = "test1"
        client_socket.sendto(message.encode(),(host,port))

        # 서버로부터 응답 받기
        response, server_address = client_socket.recvfrom(1024)
        pic_addr = response.decode()
        print(f"서버로부터 응답: {pic_addr}")

        time.sleep(1)

        message = "test2"
        client_socket.sendto(message.encode(),(host,port))

        # 서버로부터 응답 받기
        response, server_address = client_socket.recvfrom(1024)
        pic_addr = response.decode()
        print(f"서버로부터 응답: {pic_addr}")

        time.sleep(1)

        message = "test3"
        client_socket.sendto(message.encode(),(host,port))

        # 서버로부터 응답 받기
        response, server_address = client_socket.recvfrom(1024)
        pic_addr = response.decode()
        print(f"서버로부터 응답: {pic_addr}")

        
except Exception as e:
    print(f"에러 발생: {e}")

finally:
    # 소켓 닫기
    client_socket.close()