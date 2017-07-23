/*
 *  3G + GPS shield
 *
 *  Copyright (C) Libelium Comunicaciones Distribuidas S.L.
 *  http://www.libelium.com
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *  a
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see http://www.gnu.org/licenses/.
 *
 *  Version:           2.0
 *  Design:            David Gascón
 *  Implementation:    Alejandro Gallego & Victor Boria
 */

//Include ArduPi library
#include "arduPi.h"

void power_on();
int8_t sendATcommand(const char* ATcommand, const char* expected_answer1, unsigned int timeout);


int8_t answer;
int onModulePin = 2;
char gps_data[100];
int counter;


void setup()
{

  pinMode(onModulePin, OUTPUT);
  Serial.begin(115200);

  printf("Starting...\n");
  power_on();

  delay(3000);

  // starts GPS session in stand alone mode
  answer = sendATcommand("AT+CGPS=1,1", "OK", 1000);
  if (answer == 0)
  {
    printf("Error starting the GPS. The code stucks here!!\n");
    while (1);
  }

  printf("GPS session started\n");
}

void loop() {

  answer = sendATcommand("AT+CGPSINFO", "+CGPSINFO:", 1000);  // request info from GPS
  if (answer == 1)
  {

    counter = 0;
    do {
      while (Serial.available() == 0);
      gps_data[counter] = Serial.read();
      counter++;
    }
    while (gps_data[counter - 1] != '\r');
    gps_data[counter] = '\0';
    if (gps_data[0] == ',')
    {
      printf("No GPS data available\n");
    }
    else
    {
      printf("GPS data: %s\n", gps_data);
    }

  }
  else
  {
    printf("Error\n");
  }

  delay(5000);


}





void power_on()
{

  uint8_t answer = 0;

  // checks if the module is started
  answer = sendATcommand("AT", "OK", 2000);
  if (answer == 0)
  {
    // power on pulse
    digitalWrite(onModulePin, HIGH);
    delay(3000);
    digitalWrite(onModulePin, LOW);

    // waits for an answer from the module
    while (answer == 0) {
      // Send AT every two seconds and wait for the answer
      answer = sendATcommand("AT", "OK", 2000);
    }
  }

}



int8_t sendATcommand(const char* ATcommand, const char* expected_answer1, unsigned int timeout)
{

  uint8_t x = 0,  answer = 0;
  char response[100];
  unsigned long previous;

  memset(response, '\0', 100);    // Initialize the string

  delay(100);

  while ( Serial.available() > 0) Serial.read();   // Clean the input buffer

  Serial.println(ATcommand);    // Send the AT command


  x = 0;
  previous = millis();

  // this loop waits for the answer
  do
  {

    if (Serial.available() != 0) {
      response[x] = Serial.read();
      printf("%c", response[x]);
      x++;
      // check if the desired answer 1 is in the response of the module
      if (strstr(response, expected_answer1) != NULL)
      {
        printf("\n");

        answer = 1;
      }
    }
    // Waits for the answer with time out
  }
  while ((answer == 0) && ((millis() - previous) < timeout));

  return answer;
}


int main () {
  setup();
  while (1) {
    loop();
  }
  return (0);
}


