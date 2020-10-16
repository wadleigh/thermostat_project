#include <ESP8266WiFi.h>
#include <credentials.h>

  const char* ssid = WIFI_SSID;
  const char* password = WIFI_PASSWORD;

void setup (){
 
  Serial.begin(115200);
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
 
    delay(1000);
    Serial.println("Connecting..");
 
  }
 
  Serial.println(WiFi.localIP());
 
}

void loop() {
  // put your main code here, to run repeatedly:

}
