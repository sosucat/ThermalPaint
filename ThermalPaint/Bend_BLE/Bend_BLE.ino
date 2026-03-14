#include <Wire.h> 
#include "SparkFun_Displacement_Sensor_Arduino_Library.h" 
#include <bluefruit.h> // Using the built-in Adafruit/Seeed BLE library

ADS myFlexSensor; 

// 1. Create a Custom BLE Service and Characteristic
BLEService        flexService(0x19B1); 
BLECharacteristic flexChar(0x19B2);    

void setup() {
  Serial.begin(115200);
  
  // Wait for serial (timeout after 3 seconds for battery operation)
  unsigned long startMillis = millis();
  while (!Serial && millis() - startMillis < 3000); 

  Serial.println("Initializing hardware...");

  // Start I2C and Sensor
  Wire.begin();
  if (myFlexSensor.begin() == false) {
    Serial.println("No sensor detected. Check wiring!");
    while (1); 
  }
  
  // Start the Bluefruit BLE stack
  Bluefruit.begin();
  Bluefruit.setName("Bend_BLE"); // Device name seen on your phone

  // Set up the Service
  flexService.begin();

  // Set up the Characteristic (Read and Notify)
  flexChar.setProperties(CHR_PROPS_READ | CHR_PROPS_NOTIFY);
  flexChar.setPermission(SECMODE_OPEN, SECMODE_NO_ACCESS);
  flexChar.setMaxLen(15); 
  flexChar.begin();
  flexChar.write("0.00"); // Default starting value

  // Configure BLE Advertising (How the board broadcasts itself)
  Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
  Bluefruit.Advertising.addTxPower();
  Bluefruit.Advertising.addService(flexService);
  Bluefruit.ScanResponse.addName();
  
  // Start Advertising
  Bluefruit.Advertising.restartOnDisconnect(true);
  Bluefruit.Advertising.setInterval(32, 244); 
  Bluefruit.Advertising.setFastTimeout(30);   
  Bluefruit.Advertising.start(0); // 0 = Keep advertising forever
  
  Serial.println("Bluetooth device active! Waiting for a connection...");
}

void loop() {
  // Only try to read and push data if a device is connected
  if (Bluefruit.connected()) {
    
    if (myFlexSensor.available() == true) {
      
      float currentAngle = myFlexSensor.getX();
      Serial.println(currentAngle);
      
      // Convert the float to a string for easy reading on the phone
      String angleStr = String(currentAngle);
      
      // Push the new value over Bluetooth via Notification
      flexChar.write(angleStr.c_str(), angleStr.length());
      flexChar.notify(angleStr.c_str(), angleStr.length());
      
      // Small delay to prevent network congestion
      delay(40); 
    }
  }
}