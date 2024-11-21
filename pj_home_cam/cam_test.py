from picamera2 import Picamera2
import time

# 카메라 객체 생성
picam2 = Picamera2()

# 카메라 초기화
picam2.start()

i=9
# 이미지 캡처
time.sleep(2)  # 카메라 초기화 대기
picam2.capture_file("./pic/pic"+str(i)+".jpg")

# 카메라 종료
picam2.stop()