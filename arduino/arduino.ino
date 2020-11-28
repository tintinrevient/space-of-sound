#include <Arduino.h>

// knob to control the light intensity
int knobInPin = A0;
int knobInVal = 0;

// button to turn on/off the light
int buttonInPin = 8;

// photoresistor
int photoInPin = A1;
bool previousPhotoState = false;
bool getPhotocellState();

bool isLightOn = false;

int prevButtonVal = HIGH; // button up


// value to scale from [0, 1023] to [0, 255]
float scale = 255.0f / 1030.0f;

// light pin
int lightOutPin = 9;


void setup() {
    Serial.begin(9600);
    pinMode(buttonInPin, INPUT_PULLUP);
}

void loop() {
    knobInVal = analogRead(knobInPin);  // read the input pin from knob
    int buttonInVal = digitalRead(buttonInPin); // read the input pin from button
    Serial.println(buttonInVal);

    if(prevButtonVal == HIGH && buttonInVal == LOW)
        isLightOn = !isLightOn;
    prevButtonVal = buttonInVal;

    bool photoState = getPhotocellState();
    if(previousPhotoState != photoState)
        isLightOn = photoState;
    previousPhotoState = photoState;

    if(isLightOn) {
        float lightOutVal = knobInVal * scale;
        analogWrite(lightOutPin, lightOutVal);
    } else {
        analogWrite(lightOutPin, 0);
    }
}

bool getPhotocellState(){
    int photoInVal = analogRead(photoInPin); // read the input pin from photoresistor
    Serial.println(photoInVal);
    if(photoInVal < 50)
        return true;
    if(photoInVal > 100)
        return false;
}
