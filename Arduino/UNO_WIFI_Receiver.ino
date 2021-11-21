#include <SoftwareSerial.h>
#define esp_cmd_loop 10
#define esp_cmd_delay 1000

SoftwareSerial esp8266(2,3); //TX,RX

const int A_enable = 10;
const int A_dir1 = 9;
const int A_dir2 = 8;
const int B_enable = 5;
const int B_dir1 = 6;
const int B_dir2 = 7;
int motor_speed = 0;
void setup(){
  esp8266.begin(115200); // esp01 start
  esp8266.setTimeout(5000);
  
  Serial.begin(115200); 
  Serial.println("WIFI_IOT Receiver"); 

  pinMode(A_enable, OUTPUT); //motor A enable
  pinMode(A_dir1, OUTPUT); //motor A dir_1
  pinMode(A_dir2, OUTPUT); //motor A dir_2

  pinMode(B_enable, OUTPUT); //motor B enable
  pinMode(B_dir1, OUTPUT); //motor B dir_1
  pinMode(B_dir2, OUTPUT); //motor B dir_2

  digitalWrite(A_dir1, HIGH);
  digitalWrite(A_dir2, LOW);
  digitalWrite(B_dir1, HIGH);
  digitalWrite(B_dir2, LOW);

  analogWrite(A_enable, motor_speed);
  analogWrite(B_enable, motor_speed);
  esp_init();
}

void loop(){
  String IPD = "";
  int temp_speed = 0;
  if(esp8266.available()) {
    IPD = esp8266.readStringUntil('\n'); // i would actually use Serial.print() here
  }
  String parsed = IPD.substring(7, 10);
  if(parsed.length() == 3){
    temp_speed = parsed.toInt();
    if(temp_speed <= 100){
        temp_speed = 0;
    }
    Serial.println(temp_speed);
    if(temp_speed != motor_speed){
      motor_speed = temp_speed;
      analogWrite(A_enable, motor_speed);
      analogWrite(B_enable, motor_speed);
    }
  }
  
}

void esp_init(){
  String esp_target_id = "room";
  String esp_target_pw = "asdf0303";
  String esp_target_ip = "192.168.0.21";
  
  esp_cmd("AT");
  esp_cmd("AT+CWMODE=1");
  esp_cmd("AT+CWQAP");
  esp_cmd("AT+RST");
  esp_cmd("AT+CWJAP=\""+ esp_target_id + "\",\"" + esp_target_pw + "\"");
  String IP = esp_get_IP();
  Serial.println("IP: " + IP);
  delay(1000);
  esp8266.println("AT+CIPMUX=0");
  delay(1000);
  esp8266.println("AT+CIPSTART=\"TCP\",\"" + esp_target_ip + "\",54322");
  delay(5000);
}

void esp_cmd(String cmd){
  String esp_log = cmd;
  int i = 0;
  bool find_ok = false;
  for(i = 0; i < esp_cmd_loop; i++){
    esp8266.println(cmd);
    while(esp8266.available()){
      if(esp8266.find("OK")) {
        find_ok = true;
        break;
      }
    }
    if(find_ok){
      esp_log += ": Done";
      Serial.println(esp_log);
      break;
    }
    delay(esp_cmd_delay);
  }
  esp_log += ": Error";
  if(!find_ok) Serial.println(esp_log);
}

String esp_get_IP(){
  String IP="";
  char ch=0;
  while(1)
  {
    esp8266.println("AT+CIFSR");                   
    while(esp8266.available()){
      if(esp8266.find("STAIP,")){
        delay(1000);
        while(esp8266.available()){
          ch=esp8266.read();                      
          if(ch=='+') return IP;
          IP += ch;
        }
      }
    }
    delay(1000);
  }
}
