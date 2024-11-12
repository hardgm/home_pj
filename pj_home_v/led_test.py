from flask import Flask, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)

LED_PIN = 17
GPIO.setmode(GPIO.BCM)  # BCM 핀 번호 모드
GPIO.setup(LED_PIN, GPIO.OUT)  # LED_PIN을 출력 핀으로 설정

@app.route('/')
def hello_user():
    return render_template('led_on_off.html')

@app.route('/led/on')
def led_on():
    GPIO.output(LED_PIN, GPIO.HIGH)
    return 'LED ON'

@app.route('/led/off')
def led_off():
    GPIO.output(LED_PIN, GPIO.LOW)
    return 'LED OFF'


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')