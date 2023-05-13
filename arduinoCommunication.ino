int incomingByte1;  
int incomingByte2;       // a variable to read incoming serial data into
int x_rotation;
int y_rotation;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    incomingByte1 = Serial.read();
    if (Serial.available() > 0) {
      incomingByte2 = Serial.read();
    }
    x_rotation = incomingByte1;
    y_rotation = incomingByte2;

    Serial.print(x_rotation);
    Serial.print(y_rotation);
    // code that turns the motor on or off based off incoming byte 

    // code that turns servo to x_rotation

    // code that turns servo to y_rotation

  }
}