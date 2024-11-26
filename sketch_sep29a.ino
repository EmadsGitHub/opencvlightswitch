String myCmd;
// Include the Servo library 
#include <Servo.h> 
// Declare the Servo pin 
int servoPin = A1; 
int button=10;
// Create a servo object 
Servo Servo1; 
void setup() { 
   // We need to attach the servo to the used pin number 
   Servo1.attach(servoPin); 
   pinMode(button, INPUT);
   Serial.begin(9600);
}
void loop(){ 

   // Make servo go to 0 degrees 
  while(Serial.available()==0){
    Servo1.write(0);
  }
  myCmd = Serial.readStringUntil('\r');
  if (myCmd == "ON"){
    Serial.println("Working");
    Servo1.write(90); 
    delay(2000);

   }
   else if (myCmd == "OFF"){
    Serial.flush();
    Servo1.write(90); 
    delay(500);
    Servo1.write(0); 
    delay(500);
   }


   
  
   
}
