

#include <Arduino.h>

#include <math.h>
#define pin PC13
const int bufferSize =2000;
uint16_t adcValues[bufferSize];
volatile int sampleIndex = 0;
bool FLAG_MESURE=false;
 uint16_t adcValues_TX[bufferSize];
volatile uint16_t CH1=0;
volatile uint16_t CH2=0;
int count =0;
union pack {
  char raw[6];
  uint16_t data[3];
};
union pack pyload;
void Update_IT_callback(void) {  
  digitalWrite(pin, HIGH);       //100ns
  //adcValues[sampleIndex++] = analogRead(PA0);
  
  //CH1=analogRead(PA1);
  CH2=analogRead(PA2);
  CH1=(sin(2*PI*1*count++/4000)*200)+400 ;
  pyload.raw[0]=0xFF;
  pyload.raw[1]=((uint8_t*)&CH1)[0];
  pyload.raw[2]=((uint8_t*)&CH1)[1];
  pyload.raw[3]=((uint8_t*)&CH2)[0];
  pyload.raw[4]=((uint8_t*)&CH2)[1];
  pyload.raw[5]=0xFF;

  FLAG_MESURE= true;

 /* Serial.printf() ((uint8_t*)&CH1)[0], ((uint8_t*)&CH1)[1])
  ((uint8_t*)&CH2)[0], ((uint8_t*)&CH2)[1])
  
*/
digitalWrite(pin, LOW);  //100ns
/*  if (sampleIndex == bufferSize) {
    sampleIndex = 0;
    memcpy(adcValues_TX, adcValues, bufferSize * sizeof(uint16_t));
    FLAG_MESURE=true;
    
  }*/
}


void setup() {
  Serial.begin(115200);
#if defined(TIM1)
  TIM_TypeDef *Instance = TIM1;
#else
  TIM_TypeDef *Instance = TIM2;
#endif

  // Instantiate HardwareTimer object. Thanks to 'new' instanciation, HardwareTimer is not destructed when setup() function is finished.
  HardwareTimer *MyTim = new HardwareTimer(Instance);
  pinMode(PA0, INPUT_ANALOG);
  // configure pin in output mode
  pinMode(pin, OUTPUT);

  MyTim->setOverflow(4000, HERTZ_FORMAT);  // 10 Hz
  MyTim->attachInterrupt(Update_IT_callback);
  MyTim->resume();
}


void loop() {
  
  if(FLAG_MESURE==true){
    Serial.write((uint8_t*)&pyload,6);
    FLAG_MESURE=false;
   }
  }