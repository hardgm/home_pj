#include <Wire.h> //I2C 라이브러리 포함(I2C버스 초기화)
#include <LiquidCrystal_I2C.h> //LCD 모듈과의 통신을 위한 인터페이스 설정
#include <Servo.h>

LiquidCrystal_I2C lcd(0x27,20,4);
Servo servo;

int PIN_ECHO = 9;
int PIN_TRIG = 8;
bool isHighPrinted = false;

int temp_password[4] = {1,4,2,3};
int input_password[4] = {0,0,0,0};
int index = 0;

int buttonPins[] = {13,12,11,10,7};
int numButtons = 5;

int buttonState[5];
int lastButtonState[5];
unsigned long lastDebounceTime[5];
unsigned long debounceDelay = 50;

int buzzerPin = 5;


void setup()
{
  Serial.begin(9600);
  lcd.init(); // lcd 초기화
  lcd.backlight(); //lcd 백라이트 켜
  servo.attach(6);
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
                
                Serial.print("Button ");
                Serial.print(i + 1);  // 버튼 번호 출력
                Serial.println(" pressed");

                input_password[index] = i+1;
                Serial.print("index : ");
                Serial.println(index);
                index++;

                lcd.setCursor(0,1);
                  for(int j=0; j<index; j++){
                    Serial.println("p");
                    lcd.print("*");
                  } 
              }

              if(index==4){
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

                    servo.write(100);
                    delay(1000);
                    servo.write(0);

                  }else{
                    lcd.clear();
                    lcd.setCursor(0,0);
                    lcd.print("INCORRECT!");
                    lcd.setCursor(0,1);
                    lcd.print("WRONG PASSWORD!");

                    analogWrite(buzzerPin, 100);
                    delay(500);
                    analogWrite(buzzerPin, 0);
                  }
                  index = 0;
                  delay(1000);
                  lcd.clear();
                }
            }
          
            if(i==4){
              lcd.clear();
              lcd.setCursor(0,0);
              lcd.print("WHO R U?");
              analogWrite(buzzerPin, 100);
              delay(500);
              analogWrite(buzzerPin, 0);
              lcd.clear();
            }

        }
      }
      }
    // 이전 상태 저장
    lastButtonState[i] = reading;
    }

    digitalWrite(PIN_TRIG, HIGH);
		delayMicroseconds(20);
		digitalWrite(PIN_TRIG, LOW);

		while(digitalRead(PIN_ECHO) ==LOW);

		long startTime = micros();

		while(digitalRead(PIN_ECHO)== HIGH);
		long endTime = micros() - startTime;

		int distance = endTime/58;

		if(distance <10)
		{
      if (!isHighPrinted) {  // 이미 HIGH가 출력되지 않았다면
      
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("WHO R U?");
      analogWrite(buzzerPin, 100);
      delay(500);
      analogWrite(buzzerPin, 0);
      lcd.clear();

      isHighPrinted = true;  // HIGH 출력 상태로 변경
      }
		}else{
      if (isHighPrinted) {  // HIGH가 이미 출력되었다면
      isHighPrinted = false;  // LOW 출력 상태로 변경
      }
		}
}