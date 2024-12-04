#include <Wire.h> //I2C 라이브러리 포함(I2C버스 초기화)
#include <LiquidCrystal_I2C.h> //LCD 모듈과의 통신을 위한 인터페이스 설정
#include <Servo.h>
#include <SoftwareSerial.h>

int buzzerPin = 5;
Servo servo;

SoftwareSerial mySerial(2, 3);
String message = "";
String data = "";

LiquidCrystal_I2C lcd(0x27,20,4);

int PIN_ECHO = 9;
int PIN_TRIG = 8;
bool isHighPrinted = false;

int distance = 0;
unsigned long lastMeasurementTime = 0;
unsigned long measurementInterval = 100;


int temp_password[4] = {1,4,2,3};
int input_password[4] = {0,0,0,0};
int index = 0;
int arr_index = 0;

int buttonPins[] = {13,12,11,10,7};
int numButtons = 5;

int buttonState[5];
int lastButtonState[5];
unsigned long lastDebounceTime[5];
unsigned long debounceDelay = 50;

void open_door(){
  servo.write(100);
}

void lock_door(){
  servo.write(0);
}

void decode_pwd(){
  for (int i = 0; i < data.length(); i++) {
        char ch = data.charAt(i);
                    
        if (ch >= '0' && ch <= '9') {
          int num = ch - '0';  // 문자 '0'을 빼면 해당 문자의 정수 값
          temp_password[arr_index] = num;  // 배열에 삽입
          arr_index++;  // 배열 인덱스 증가
        }
      }
    arr_index=0;
}

void compare_pwd(){
        if(
        (temp_password[0]==input_password[0]) &&
        (temp_password[1]==input_password[1]) &&
        (temp_password[2]==input_password[2]) &&
        (temp_password[3]==input_password[3])
        ){
          lcd.clear();
          lcd.setCursor(0,0);
          lcd.print("PASSWORD CORRECT!");
          lcd.setCursor(0,1);
          lcd.print("WELCOME!");

          message = "pwd_comp_corr";
          mySerial.println(message);
          open_door();
          
          delay(500);

        }else{
          lcd.clear();
          lcd.setCursor(0,0);
          lcd.print("INCORRECT!");
          lcd.setCursor(0,1);
          lcd.print("WRONG PASSWORD!");

          message = "pwd_comp_err";
          mySerial.println(message);

          analogWrite(buzzerPin, 100);
          delay(500);
          analogWrite(buzzerPin, 0);

          
        }
                  
        delay(1000);
        lcd.clear();
}

void bell_pushed(){
  
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("HOST WAIT !!");

  message = "bell";
  mySerial.println(message);

  analogWrite(buzzerPin, 100);
  delay(500);
  analogWrite(buzzerPin, 0);
  
  lcd.clear();
  lcd.setCursor(0,1);
  for(int j=0; j<index; j++){
    lcd.print("*");
  } 

}


void sonic_touched(){
  
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("HELLO");

  /*
  message = "sonic";
  mySerial.println(message);
  */
  delay(500);

  lcd.clear();
  lcd.setCursor(0,1);
  for(int j=0; j<index; j++){
    lcd.print("*");
  } 


}


void setup()
{
  Serial.begin(9600);
  mySerial.begin(9600);

  lcd.init(); // lcd 초기화
  lcd.backlight(); //lcd 백라이트 켜
  
  servo.attach(6);
  servo.write(0);

  pinMode(buzzerPin, OUTPUT);

  
  pinMode(PIN_ECHO, INPUT);
	pinMode(PIN_TRIG, OUTPUT);
  
  
  for (int i = 0; i < numButtons; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
    buttonState[i] = HIGH;  // 초기 상태는 HIGH (버튼이 눌리지 않았을 때)
    lastButtonState[i] = HIGH;  // 초기 상태는 HIGH
    lastDebounceTime[i] = 0;  // 초기 시간 설정
  }

}
void loop(){

  if (mySerial.available()>0) {

    data = mySerial.readString();  // 데이터 읽기
    //추후 초인종 관련 기능 구현시 data 신호를 받아 if문으로 처리.
    //관련 작업 길어질 경우 별도 함수로 분리.
    //위에서 만든 if문의 else 밑으로 밑에 있는 구문 삽입.

    if(data=="openDoor"){
      open_door();
    }else if(data=="lockDoor"){
      lock_door();
    }else{
      decode_pwd();
      compare_pwd();
    }

  }
                
    lcd.setCursor(0,0);
    lcd.print("INPUT PASSWORD !");
          
    for (int i = 0; i < numButtons; i++) {
    int reading = digitalRead(buttonPins[i]);

    // 버튼 상태가 바뀌었을 때
    if (reading != lastButtonState[i]) {
      lastDebounceTime[i] = millis();  // 상태 변화 시간 기록
    }

    // 디바운싱 시간 이후에만 상태 업데이트
    if ((millis() - lastDebounceTime[i]) > debounceDelay) {

      if (reading != buttonState[i]) {
        buttonState[i] = reading;  // 버튼 상태 업데이트

      if(buttonState[i]==LOW){
        // 버튼이 눌렸을 때
            if(i>=0 && i<=3){
          
              if(index<4){
                input_password[index] = i+1;
                index++;

                lcd.setCursor(0,1);
                  for(int j=0; j<index; j++){
                    lcd.print("*");
                  } 
              }

              if(index==4){
                message = "pwd_comp";
                mySerial.println(message);
                index=0;
              }
            }
          
            if(i==4){
              bell_pushed();
            }

        }
      }
      }
    // 이전 상태 저장
    lastButtonState[i] = reading;
    }

    
    if (millis() - lastMeasurementTime >= measurementInterval) {
      lastMeasurementTime = millis();  // 마지막 측정 시간 기록

      // 초음파 송신
      digitalWrite(PIN_TRIG, HIGH);
      delayMicroseconds(20);
      digitalWrite(PIN_TRIG, LOW);

      // 초음파 수신 대기 (비블로킹)
      long startTime = micros();
      while (digitalRead(PIN_ECHO) == LOW) {
        if (micros() - startTime > 10000) {  // 타임아웃 설정 (10ms)
          distance = -1;
          Serial.println("TIMEOUT");
          break;
        }
    }
    
    if(distance != -1){
      startTime = micros();
      while (digitalRead(PIN_ECHO) == HIGH);
      long endTime = micros() - startTime;

      distance = endTime / 58;  // 거리 계산 (cm 단위)
    }
  }

  if(distance != -1){
		if(distance < 50)
		{
      if (!isHighPrinted) {  // 이미 HIGH가 출력되지 않았다면
      sonic_touched();
      isHighPrinted = true;  // HIGH 출력 상태로 변경
      }
		}else{
      if (isHighPrinted) {  // HIGH가 이미 출력되었다면
      isHighPrinted = false;  // LOW 출력 상태로 변경
      }
		}
  }else{
    distance = 0;
  }
    
}