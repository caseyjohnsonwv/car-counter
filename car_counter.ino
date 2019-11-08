const int trigPin = 3;
const int echoPin = 2;
const long distThreshold = 96.0;
const unsigned long timeThreshold = 90000.0;
unsigned long postTime;
long duration,inches;
int counter;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  counter = 0;
  postTime = millis();
}

void loop() {
  Serial.println(counter);

  //quick HIGH pulse searches for an object
  digitalWrite(trigPin,LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin,HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin,LOW);

  //read result from ultrasonic sensor
  duration = pulseIn(echoPin,HIGH);
  inches = duration/148;

  //determine if distance is within distThreshold
  if (inches <= distThreshold) {
    counter += 1;
    //determine if data should be sent to server
    if (millis() - postTime > timeThreshold) {
      /*
       * Send an HTTP POST request to a Flask app on Heroku!
       */
    }
    delay(1000);
  }

  //wait to test again
  delay(70);
}
