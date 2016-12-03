#include <Adafruit_NeoPixel.h>

// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// released under the GPLv3 license to match the rest of the AdaFruit NeoPixel library

// Which pin on the Arduino is connected to the NeoPixels?

#define PIN1            4
#define PIN2            7

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS1      1
#define NUMPIXELS2      8

// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
// example for more information on possible values.
Adafruit_NeoPixel toplights = Adafruit_NeoPixel(NUMPIXELS1, PIN1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel scanlights = Adafruit_NeoPixel(NUMPIXELS2, PIN2, NEO_GRB + NEO_KHZ800);

int topVal = 0; // creates an integer called val, and assigns it a value of 0.
int scanVal = 0;
byte rasIn = 0;
int blinky = 0;
int toplooping = true;
int scanlooping = true;
int topPrevMillis = 0;
int scanPrevMillis = 0;
int topI = 0;
int scanI = 0;

int topBlinkDelay = 30;
int scanBlinkDelay = 1;

int scanRedColor = 0;
int scanGreenColor = 255;
int scanBlueColor = 0;


void setup() {
  toplights.begin();
  scanlights.begin(); // This initializes the NeoPixel library.
  //  pinMode(rasPin, INPUT);
  Serial.begin(9600);
  scanlooping = true;

}

void toploop(unsigned long currentMillis){
  if ((topVal == 1) && (currentMillis-topPrevMillis >= topBlinkDelay)){
    if(topI >= 255){
      topVal = 0;
    } 
    else {
      toplights.setPixelColor(0, toplights.Color(0, 255, 0));
      toplights.setBrightness(topI);
      toplights.show();
      topI++;
    }
    topPrevMillis = currentMillis;
  }
  else if ((topVal == 0) && (currentMillis-topPrevMillis >= topBlinkDelay)){
    if(topI <= 0){
      topVal = 1;
    } 
    else {
      toplights.setPixelColor(0, toplights.Color(0, 255, 0));
      toplights.setBrightness(topI);
      toplights.show();
      topI --;
    }
    topPrevMillis = currentMillis;
  }
}

void scanloop(unsigned long currentMillis){
  if ((scanVal == 0) && (currentMillis-scanPrevMillis >= scanBlinkDelay)){
    if(scanI >= 255){
      scanVal = 1;
    } 
    else {
      for (int i = 0; i < NUMPIXELS2; i++) {
        scanlights.setPixelColor(i, scanlights.Color(scanRedColor, scanGreenColor, scanBlueColor)); // Moderately bright green color.
      }
      scanlights.setBrightness(scanI);
      scanlights.show();
      scanI++;
    }
    scanPrevMillis = currentMillis;
  }
  else if ((scanVal == 1) && (currentMillis-scanPrevMillis >= scanBlinkDelay)){
    if(scanI <= 0){
      scanVal = 0;
      scanlooping = false;
      scanI = 0;
    } 
    else {
      for (int i = 0; i < NUMPIXELS2; i++) {
        scanlights.setPixelColor(i, scanlights.Color(scanRedColor, scanGreenColor, scanBlueColor)); // Moderately bright green color.
      }
      scanlights.setBrightness(scanI);
      scanlights.show();
      scanI --;
    }
    scanPrevMillis = currentMillis;
  }
}

void theaterChase(uint32_t c, unsigned long currentMillis) {
  if (currentMillis-scanPrevMillis >= scanBlinkDelay){
    for (int j=0; j<10; j++) {  //do 10 cycles of chasing
      for (int q=0; q < 3; q++) {
        for (uint16_t i=0; i < scanlights.numPixels(); i=i+3) {
          scanlights.setPixelColor(i+q, c);    //turn every third pixel on
        }
        scanlights.show();

        //      delay(wait+50);

        for (uint16_t i=0; i < scanlights.numPixels(); i=i+3) {
          scanlights.setPixelColor(i+q, scanlights.Color(0, 0, 255));        //turn every third pixel off
        }
        for (uint16_t i=0; i < scanlights.numPixels(); i=i+2) {
          scanlights.setPixelColor(i+q, scanlights.Color(0, 0, 200));        //turn every third pixel off
        }
      }
    }
  }
}

void loop() {
  // For a set of NeoPixels the first NeoPixel is 0, second is 1, all the way up to the count of pixels minus one.
  //  val = digitalRead(rasPin);
  unsigned long currentMillis = millis();
  if(Serial.available()){
    rasIn = (Serial.read());
    if (rasIn == '5'){
      scanlooping = true;
      scanPrevMillis = currentMillis;
      scanRedColor = 0;
      scanGreenColor = 255;
      scanBlueColor = 0;
    } 
    else if (rasIn = '6'){
      scanlooping = true;
      scanPrevMillis = currentMillis;
      scanRedColor = 255;
      scanGreenColor = 0;
      scanBlueColor = 0;
    }
  } 
  if(toplooping){
    toploop(currentMillis);
  }
  if(scanlooping){
    scanloop(currentMillis);
  }
  if(!scanlooping){
    for (int i = 0; i < NUMPIXELS2; i++) {
      scanlights.setPixelColor(i, scanlights.Color(0, 0, 255));
      scanlights.setBrightness(255);
      scanlights.show();
    }
  }
}

