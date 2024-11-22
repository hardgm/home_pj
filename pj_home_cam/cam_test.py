from picamera2 import Picamera2
from datetime import datetime
import time

# 카메라 객체 생성
picam2 = Picamera2()

# 카메라 초기화
picam2.start()

# 이미지 캡처
time.sleep(2)  # 카메라 초기화 대기

name = datetime.now().strftime("%m-%d-%H-%M-%S")

picam2.capture_file("../pj_home_v/static/images/"+name+".jpg")

# 카메라 종료
picam2.stop()