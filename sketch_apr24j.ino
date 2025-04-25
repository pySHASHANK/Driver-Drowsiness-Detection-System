// Arduino Nano Drowsiness Alert Code

int buzzerPin = 3;  // Connect buzzer to D3
int ledPin = 4;     // Connect LED to D4

void setup() {
  pinMode(buzzerPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);  // Start Serial at 9600 baud
}

void loop() {
  if (Serial.available()) {
    char data = Serial.read();

    if (data == 'H') {
      digitalWrite(buzzerPin, HIGH);
      digitalWrite(ledPin, HIGH);
    } 
    else if (data == 'L') {
      digitalWrite(buzzerPin, LOW);
      digitalWrite(ledPin, LOW);
    }
  }
}
