/*FollowMe: A program that turns the microcontroller (and some external accessories)
 * into a (sort of) clone of the classic 'Simon' game. 
*/

//Define the maximum length of the pattern. Note that since array indices start at 0
//instead of 1, the length of the pattern is actually 1 more than the number given here.
const int patternLen = 19; 
//Define the delay (in milliseconds) used for the spectrum effect
const int delayLen = 0;

unsigned char pattern[patternLen]; //Initialize the array that will store the pattern
const int spkrPin = 16; //The pin the speaker is connected to

void setup() {
  Serial.begin(115200); //Begin serial for debug output at 115200 baud
  
  //Set up the buttons' pins for input
  pinMode(4, INPUT_PULLUP);
  pinMode(5, INPUT_PULLUP);
  pinMode(2, INPUT_PULLUP);
  pinMode(0, INPUT_PULLUP);

  pinMode(15, INPUT);
  
  //Set up the tone output pin
  pinMode(spkrPin, OUTPUT);

  //Set up the LED output pins
  pinMode(14, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);

  //Randomize the RNG from the analog pin
  randomSeed(analogRead(A0));

  delay(1000);
}

void loop() {
  ////////////////////- Setup Phase -////////////////////
  ////Setup phase takes care of things like writing  ////
  ////  the next value to 'pattern', generating the  ////
  ////  appropriate tone for the value, lighting the ////
  ////  correct LED for the tone (eventually), etc.  ////
  ///////////////////////////////////////////////////////
  static int i = 0; //Initialize the counter variable
  int randVal = random(1, 5); //Store a random number between 1 and 4 to 'randVal'

  pattern[i] = randVal; //Write the value of 'randVal' to current index of 'pattern'

  Serial.print("pattern:\t");
  for(int serialOut = 0; serialOut <= patternLen; serialOut++){
      Serial.print(pattern[serialOut]);
  }
  Serial.println();
  
  for(int pos = 0; pos <= i; pos++){
    int curVal = pattern[pos]; //Read the value of the current index into 'curVal'
    
    switch(curVal){
      case 1:
        tone(spkrPin, 523, 500);
        digitalWrite(14, LOW);
        delay(500);
        digitalWrite(14, HIGH);
        break;
      case 2:
        tone(spkrPin, 659, 500);
        digitalWrite(12, LOW);
        delay(500);
        digitalWrite(12, HIGH);
        break;
      case 3:
        tone(spkrPin, 784, 500);
        digitalWrite(13, LOW);
        delay(500);
        digitalWrite(13, HIGH);
        break;
      case 4:
        tone(spkrPin, 1047, 500);
        digitalWrite(14, LOW);
        digitalWrite(12, LOW);
        digitalWrite(13, LOW);
        delay(500);
        digitalWrite(14, HIGH);
        digitalWrite(12, HIGH);
        digitalWrite(13, HIGH);
        break;
    }
    delay(250);
    noTone(spkrPin);
    delay(125);
  }
  ////////////////////- End Setup Phase -////////////////////

  
  ////////////////////- Interract Phase -////////////////////
  ////Interract phase takes care of things like handling ////
  ////  the button inputs (E.G. playing the appropriate  ////
  ////  tone for the appropriate button, lighting the    ////
  ////  appropriate LED [eventually]), checking the order////
  ////  of the pattern entered, and acting on that order.////
  ///////////////////////////////////////////////////////////
  static unsigned char inPattern[patternLen]; //Initialize an array to hold the input pattern

  int authCode = 0;
  static bool willBreak = false;
  static int btnCount = 0;
  static bool authorizedCheater = false;

  unsigned long t2 = 0;
  
  digitalWrite(14, HIGH);
  digitalWrite(12, HIGH);
  digitalWrite(13, HIGH);
  
  for(int inPos = 0; inPos <= i; inPos++){
    
    if (digitalRead(15) == HIGH){ //Cheater authorization code /NOTE: not working 
      unsigned long t = millis();
      if (willBreak == true) break;
      Serial.println("Awaiting CHEATER AUTHORIZATION..."); 
      
      while (digitalRead(4) == HIGH and digitalRead(5) == HIGH and digitalRead(2) == HIGH and digitalRead(0) == HIGH){
        t2 = millis();
        if (t2 - t == 5000) willBreak = true;  Serial.println("UNAUTHORIZED CHEATER DETECTED!!!");
        yield();
      }

      t = t2;

      if (digitalRead(4) == LOW) authCode += 4; btnCount ++;
      if (digitalRead(5) == LOW) authCode += 6; btnCount ++;
      if (digitalRead(2) == LOW) authCode += 11; btnCount ++;
      if (digitalRead(0) == LOW) authCode += 18; btnCount ++;

      if (authCode == 46 and btnCount == 4) bool authorizedCheater = true; willBreak = true; Serial.println("CHEATER AUTHORIZED");
    }
    
    //Do nothing until a button is pressed
    while (digitalRead(4) == HIGH and digitalRead(5) == HIGH and digitalRead(2) == HIGH and digitalRead(0) == HIGH){
      yield();          
    }
    
    if (digitalRead(4) == LOW){
      inPattern[inPos] = 1;
      tone(spkrPin, 523, 500);
      digitalWrite(14, LOW);
      delay(500);
      digitalWrite(14, HIGH);
    }
    else if (digitalRead(5) == LOW){
      inPattern[inPos] = 2;
      tone(spkrPin, 659, 500);
      digitalWrite(12, LOW);
      delay(500);
      digitalWrite(12, HIGH);
    }
    else if (digitalRead(2) == LOW){
      inPattern[inPos] = 3;
      tone(spkrPin, 784, 500);
      digitalWrite(13, LOW);
      delay(500);
      digitalWrite(13, HIGH);
    }
    else if (digitalRead(0) == LOW){
      inPattern[inPos] = 4;
      tone(spkrPin, 1047, 500);
      digitalWrite(14, LOW);
      digitalWrite(12, LOW);
      digitalWrite(13, LOW);
      delay(500);
      digitalWrite(14, HIGH);
      digitalWrite(12, HIGH);
      digitalWrite(13, HIGH);
    }
    
    delay(250);
    noTone(spkrPin);
    delay(125);

    if (authorizedCheater == true and digitalRead(4) == LOW and digitalRead(2) == LOW and digitalRead(0) == LOW) noiseSuccessFail("Success");
    
    if (inPattern[inPos] != pattern[inPos]) noiseSuccessFail("Failure");
    if (inPattern[patternLen] != 0 and inPattern[patternLen] == pattern[patternLen]) noiseSuccessFail("Success");
    }
  
  Serial.print("inPattern:\t");
    for(int serialOut = 0; serialOut <= patternLen; serialOut++){
      Serial.print(inPattern[serialOut]);
    }
    Serial.println();
  ////////////////////- End Interract Phase -////////////////////

  
  ////////////////////- Final Phase -////////////////////
  ////Final phase does any cleanup that needs doing  ////
  ////  before looping back around, such as          ////
  ////  incrementing the counter variable and such.  ////
  ///////////////////////////////////////////////////////
  noTone(spkrPin);
  i++;
  delay(500);
  ////////////////////- End Final Phase -////////////////////
}

void noiseSuccessFail(String statusIn){
  if (statusIn.equalsIgnoreCase("success")){
    tone(spkrPin, 523);
    delay(125);
    noTone(spkrPin);
    delay(25);
    tone(spkrPin, 659);
    delay(125);
    noTone(spkrPin);
    delay(25);
    tone(spkrPin, 784);
    delay(125);
    noTone(spkrPin);
    delay(25);
    tone(spkrPin, 1047);
    delay(125);
    noTone(spkrPin);
    delay(25);
    tone(spkrPin, 1047);
    delay(125);
    noTone(spkrPin);
    delay(25);
    tone(spkrPin, 1047);
    delay(125);
    noTone(spkrPin);
    delay(25);
    tone(spkrPin, 784);
    delay(125);
    noTone(spkrPin);
    delay(25);
    tone(spkrPin, 784);
    delay(125);
    noTone(spkrPin);
    delay(25);
    tone(spkrPin, 784);
    delay(125);
    noTone(spkrPin);
    delay(25);
    tone(spkrPin, 659);
    delay(125);
    noTone(spkrPin);
    delay(25);
    tone(spkrPin, 784);
    delay(125);
    noTone(spkrPin);
    delay(25);
    tone(spkrPin, 659);
    delay(125);
    noTone(spkrPin);
    delay(25);
    tone(spkrPin, 523);
    delay(1000);
    noTone(spkrPin);
    rainbowInit(14, 12, 13, delayLen); //Call the routine that produces a nice spectrum effect
    ESP.restart();
  }
  else if (statusIn.equalsIgnoreCase("failure")){
    for(int toneOut = 500; toneOut > 60; toneOut -= 10){ //Generate a descending tone
      tone(spkrPin, toneOut);
      delay(50);
    }
    delay(1000);
    ESP.restart();
  }
}

void rainbowInit(int pinRed, int pinGrn, int pinBlu, int delayTime){
  analogWrite(pinRed, 1023);
  analogWrite(pinGrn, 1023);
  analogWrite(pinBlu, 1023);

  for (int redVal = 1023; redVal >= 0; redVal--){
    analogWrite(pinRed, redVal);
    while (digitalRead(15) == HIGH) yield();
    delay(delayTime);
  }
   rainbowMain(pinRed, pinGrn, pinBlu, delayTime);
}

void rainbowMain(int pinRed, int pinGrn, int pinBlu, int delayTime){
  while (true){
    for (int grnVal = 1023; grnVal >= 0; grnVal--){
      analogWrite(pinGrn, grnVal);
      while (digitalRead(15) == HIGH) yield();
      if (digitalRead(4) == LOW or digitalRead(5) == LOW or digitalRead(2) == LOW or digitalRead(0) == LOW) break;
      delay(delayTime);
    }
    for (int redVal = 0; redVal < 1024; redVal++){
      analogWrite(pinRed, redVal);
      while (digitalRead(15) == HIGH) yield();
      if (digitalRead(4) == LOW or digitalRead(5) == LOW or digitalRead(2) == LOW or digitalRead(0) == LOW) break;
      delay(delayTime);
    }
    for (int bluVal = 1023; bluVal >= 0; bluVal--){
      analogWrite(pinBlu, bluVal);
      while (digitalRead(15) == HIGH) yield();
      if (digitalRead(4) == LOW or digitalRead(5) == LOW or digitalRead(2) == LOW or digitalRead(0) == LOW) break;
      delay(delayTime);
    }
    for (int grnVal = 0; grnVal < 1023; grnVal++){
      analogWrite(pinGrn, grnVal);
      while (digitalRead(15) == HIGH) yield();
      if (digitalRead(4) == LOW or digitalRead(5) == LOW or digitalRead(2) == LOW or digitalRead(0) == LOW) break;
      delay(delayTime);
    }
    for (int redVal = 1023; redVal >= 0; redVal--){
      analogWrite(pinRed, redVal);
      while (digitalRead(15) == HIGH) yield();
      if (digitalRead(4) == LOW or digitalRead(5) == LOW or digitalRead(2) == LOW or digitalRead(0) == LOW) break;
      delay(delayTime);
    }
    for (int bluVal = 0; bluVal < 1023; bluVal++){
      analogWrite(pinBlu, bluVal);
      while (digitalRead(15) == HIGH) yield();
      if (digitalRead(4) == LOW or digitalRead(5) == LOW or digitalRead(2) == LOW or digitalRead(0) == LOW) break;
      delay(delayTime);
    }
  }
}
