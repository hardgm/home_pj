import socket
from picamera2 import Picamera2
from datetime import datetime
import time
from PIL import Image

host = '127.0.0.1'
port = 65432

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, port))
print(f"서버가 {host}:{port}에서 대기하고 있습니다...")

try:
    picam2 = Picamera2()
    picam2.start()
    time.sleep(2)

    while True:
        message, client_address = server_socket.recvfrom(1024)
        message_str = message.decode()
        print(f"클라이언트({client_address})로부터 메시지 수신: {message_str}")
        name = datetime.now().strftime("%m-%d-%H-%M-%S")
        image_path = f"../pj_home_v/static/images/{name}.jpg"

        #picam2.capture_file("../pj_home_v/static/images/"+name+".jpg")
        picam2.capture_file(image_path)

        with Image.open(image_path) as img:
            # 이미지를 180도 회전
            rotated_img = img.rotate(180)
            
            # 회전된 이미지를 다시 저장 (같은 경로에 덮어쓰거나 다른 이름으로 저장 가능)
            rotated_img.save(image_path)
        
        server_socket.sendto(name.encode(),client_address)

except Exception as e:
    print(f"에러 발생: {e}")

finally:
    picam2.stop()
    server_socket.close()