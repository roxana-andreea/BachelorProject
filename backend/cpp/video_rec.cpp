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
int8_t sendATcommand2(const char* ATcommand, const char* expected_answer1, const char* expected_answer2, unsigned int timeout);

int8_t answer;
int onModulePin = 2;


void setup()
{

  pinMode(onModulePin, OUTPUT);
  Serial.begin(115200);

  printf("Starting...\n");
  power_on();

  delay(3000);


  // Starts the camera
  answer = sendATcommand2("AT+CCAMS", "OK", "CAMERA NO SENSOR", 3000);
  if (answer == 1)
  {
    // Sets resolution
    sendATcommand2("AT+CCAMSETD=320,240", "OK", "ERROR", 2000);

    // Sets frame rate
    sendATcommand2("AT+CCAMSETF=2", "OK", "ERROR", 2000);

    // Takes a picture, but not saved it
    answer = sendATcommand2("AT+CCAMRS", "OK", "ERROR", 5000);
    delay(1000);
    if (answer == 1)
    {
      delay(5000);
      sendATcommand2("AT+CCAMRP", "OK", "ERROR", 2000);
      delay(5000);
      sendATcommand2("AT+CCAMRR", "OK", "ERROR", 2000);
      delay(5000);
      sendATcommand2("AT+CCAMRE", "OK", "ERROR", 2000);

    }
    else if (answer == 2)
    {
      printf("Camera invalid state\n");
    }
    else
    {
      printf("Error taking the picture\n");
    }

    sendATcommand("AT+CCAME", "OK", 2000);
  }
  else if (answer == 2)
  {
    printf("Camera not detected\n");
  }
  else
  {
    printf("Error starting the camera\n");
  }




}

void loop() {

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

  uint16_t x = 0,  answer = 0;
  char response[1000];
  unsigned long previous;

  memset(response, '\0', 100);    // Initialize the string

  delay(100);

  while ( Serial.available() > 0) Serial.read();   // Clean the input buffer

  Serial.println(ATcommand);    // Send the AT command


  x = 0;
  previous = millis();

  // this loop waits for the answer
  do {

    if (Serial.available() != 0) {
      response[x] = Serial.read();
      printf("%c", response[x]);
      x++;
      // check if the desired answer is in the response of the module
      if (strstr(response, expected_answer1) != NULL)
      {
        printf("\n");
        answer = 1;
      }
    }
    // Waits for the asnwer with time out
  }
  while ((answer == 0) && ((millis() - previous) < timeout));

  return answer;
}



int8_t sendATcommand2(const char* ATcommand, const char* expected_answer1, const char* expected_answer2, unsigned int timeout)
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
      // check if the desired answer 2 is in the response of the module
      if (strstr(response, expected_answer2) != NULL)
      {
        printf("\n");
        answer = 2;
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

