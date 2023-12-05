/*
 * PROGRAM : ESP8266 SERVER WITH AMG8833 GRID EYE
 * AUTHOR  : LIYANAGE KALANA PERERA
 * DATE    : 2023.12.4 --> 17:35 PM
 * 
 * 
 * NOTE: --> THIS SCKETCH WILL TURN OUR ESP8266 INTO A WEB SERVER THAT WE CAN USE 
 *           AS A TELEMETRY SYSTEM.
 *       --> AMG8833 THERMAL IMAGING SENSOR IS CONNECTED TO THE SERVER AND WE CAN GET
 *           THERMAL DATA VIA WLAN NETWORK. 
 *       --> TO AVOID ANY ISSUES, USE CORRECT WIFI SSID AND PASSWORD.
 *       
 * 
 * PIN CONNECTION FROM AMG8833 TO ESP8266
 * 
 * VCC                 3V3
 * GND                 GND
 * SCL                 D1 
 * SDA                 D2 
 * INT                 N/C
 * AD0                 N/C OR PULLED-DOWN IF ADD IS 0x68
 * 
 * 
*/

#include <ESP8266WiFi.h>

int HEATSETS = 0;// NUMBER OF HEAT PIXEL READINGS.
String  ClientRequest;
WiFiServer server(80);

// AMG8833 thermal sensor related   
   #include <Adafruit_AMG88xx.h>
   Adafruit_AMG88xx amg;
   float pixels [AMG88xx_PIXEL_ARRAY_SIZE]; // Getting the 64 bit Pixels.
   
void setup() 
{
  ClientRequest = "";
  Serial.begin(9600);
  WiFi.disconnect();
  delay(3000);
  Serial.println("START");
  WiFi.begin("SLT-4G_1F24E4","6C22B7E5"); // HOME NETWORK.
  //WiFi.begin("WIFI_SSID","PASSWORD"); // DEFAULT NETWORK.
  //WiFi.begin("ARK","ARK@5010110"); // OFFICE NETWORK.
  while ((!(WiFi.status() == WL_CONNECTED))){
    delay(300);
    Serial.print("..");
  }
  Serial.println("CONNECTED");
  Serial.println("AVAILABLE IP IS:");
  Serial.println((WiFi.localIP().toString()));
  delay(5000);
  server.begin();
  Serial.println (); 
  Serial.println (F("AMG88xx PIXELS"));

  bool status;
  status = amg.begin ();                                                                // default settings
  if (!status) 
  {
    Serial.println("COULD NOT FIND A VALID AMG88xx SENSOR, CHECK WIRING!");
    while (1);
  }
  Serial.println ("-- PIXEL TEST --");
  Serial.println ();
  delay (100);                                                                         // let sensor boot up
}
   
void loop() 
{ 
  //------------------------------------------------- THERMAL READING PART. 
  // READING UPTO 100 HEATSETS. BUT CURRUNTLY COMPUTER CAN ONLY PROCESS ONE HEATSET.
  if(HEATSETS < 100)
  {  
   amg.readPixels(pixels);                                                              // read all the pixels
   Serial.println("[");
   for(int i=1; i<=AMG88xx_PIXEL_ARRAY_SIZE; i++)
     {
      Serial.print (pixels[i-1]);
      Serial.print (", ");
      if ( i%8 == 0 ) Serial.println();
      }
   Serial.println ("]");
  }
   //------------------------------------------------- NETWORK PART.   
   WiFiClient client = server.available();
    if (!client) { return; }
    while(!client.available()){  delay(1); }
    ClientRequest = (client.readStringUntil('\r'));
    ClientRequest.remove(0, 5);
    ClientRequest.remove(ClientRequest.length()-9,9);
    Serial.println("Inbound Request");
    Serial.println(ClientRequest);
    // WE CAN USE THIS "client.println" TO WRITE TO CLIENT.
    client.println("HTTP/1.1 200 OK");
    client.println("");
    //----------------------------------------------- PRINTING THE THERMAL DATA (FOR PROCESS).
    //client.println("[");
    for(int i=1; i<=AMG88xx_PIXEL_ARRAY_SIZE; i++)
    {
     client.println(pixels[i-1]);
     delay(1);
     client.flush(); 
     //if ( i%1 == 0 ) client.println(" ");
     delay(100);
   } 
   delay(1000);
   HEATSETS++;// INCREMENT THE HEATSETS VALUE.
}
