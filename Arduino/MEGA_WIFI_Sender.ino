#define esp8266 Serial2
#define esp_cmd_loop 10
#define esp_cmd_delay 1000

#include <pm2008_i2c.h>
PM2008_I2C pm2008_i2c;

#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

String result_dust = "PM 1.0 : -1\nPM 2.5 : -1\n,PM 10 : -1\n";
String result_ht = "Humidity : -1\nTemperature : -1\n";
void setup()
{
  pm2008_i2c.begin(); // dust sensor start
  pm2008_i2c.command();

  dht.begin();
  
  esp8266.begin(115200); // esp01 start
  esp8266.setTimeout(5000);
  
  Serial.begin(115200); 
  Serial.println("WIFI_IOT Sender"); 
  esp_init();
  
}
void loop()
{
  uint8_t ret = pm2008_i2c.read();
  if(ret == 0){
      result_dust = "PM1.0: ";
      result_dust.concat(pm2008_i2c.pm1p0_grimm);
      result_dust.concat(" ");
      result_dust.concat("PM2.5: ");
      result_dust.concat(pm2008_i2c.pm2p5_grimm);
      result_dust.concat(" ");
      result_dust.concat("PM10: ");
      result_dust.concat(pm2008_i2c.pm10_grimm);
      result_dust.concat(" ");
  }
  float result_humid = dht.readHumidity();
  float result_temp  = dht.readTemperature();

  if(!isnan(result_humid) && !isnan(result_temp)){
      result_ht = "Humidity: ";
      result_ht.concat(result_humid);
      result_ht.concat(" ");
      result_ht.concat("Temperature: ");
      result_ht.concat(result_temp);
      result_ht.concat(" ");
  }

  String result = result_dust;
  result.concat(result_ht);

  
  if(esp8266.available()) // check if the esp is sending a message 
  {
    Serial.write(esp8266.read());
  }
  else{
    esp8266.println("AT+CIPSEND=" + String(result.length()) );
    delay(1000);
    esp8266.println(result);
    delay(3000);
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
  esp8266.println("AT+CIPSTART=\"TCP\",\"" + esp_target_ip + "\",54321");
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
