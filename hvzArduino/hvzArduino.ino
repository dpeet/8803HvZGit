// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// released under the GPLv3 license to match the rest of the AdaFruit NeoPixel library

#include <Adafruit_NeoPixel.h>


// Which pin on the Arduino is connected to the NeoPixels?
// On a Trinket or Gemma we suggest changing this to 1
#define PIN            4

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS      1

// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals.
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest
// example for more information on possible values.
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

int delayval = 500; 

int rasPin = 8; // defines digital pin 8 as rasPin  
int val = 0; // creates an integer called val, and assigns it a value of 0. 
  

void setup() {
  pixels.begin(); // This initializes the NeoPixel library.
  pinMode(rasPin, INPUT);
  Serial.begin(9600); 
}

void loop() {
  // For a set of NeoPixels the first NeoPixel is 0, second is 1, all the way up to the count of pixels minus one.
//  val = digitalRead(rasPin);
  Serial.println(val);
  delay(4000);
  if(val == 1){
    
    for(int i=0;i<NUMPIXELS;i++){
      pixels.setPixelColor(i, pixels.Color(0, 255, 0)); // Moderately bright green color.
      pixels.show(); // This sends the updated pixel color to the hardware.
      delay(delayval);
      
    }
    val = 0;
  } else {
    for(int i=NUMPIXELS;i>=0;i--){
      pixels.setPixelColor(i, pixels.Color(0, 5, 0));
      pixels.show(); // This sends the updated pixel color to the hardware.
      delay(delayval);
    }
    val = 1;
  }
}
