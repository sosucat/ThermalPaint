int analogPin0 = A0;
int analogPin1 = A1;
int val0 = 0;
int val1 = 0;
int temp0 = 0;
int temp1 = 0;
int count = 0;

void setup() {
  Serial.begin(115200); // setup serial
}

void loop() {
  val0 = 0;
  count = 0;
  for(int i = 0; i < 50; i++) {
    temp0 = analogRead(analogPin0);
    if(temp0 > 100) {
      val0 += temp0;
      count ++;
    }
  }
  val0 /= count;

  val1 = 0;
  count = 0;
  for(int i = 0; i < 50; i++) {
    temp1 = analogRead(analogPin1);
    if(temp1 > 100) {
      val1 += temp1;
      count ++;
    }
  }
  val1 /= count;
  
  // Serial.print("510\t550\t");
  Serial.print(val1);
  Serial.print(",");
  Serial.println(val0);
}
