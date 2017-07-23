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

//Write here you server and account data
const char server[ ] = "*********";
const char user_name[ ] = "*********";
const char password[ ] = "*********";
const char port[ ] = "***";

//Write here you SIM card data
const char sim_pin[] = "****";
const char sim_apn[] = "*********";
const char sim_user[] = "*********";
const char sim_password[] = "*********";

int answer, counter;
int onModulePin = 2;    // the pin to switch on the module (without press on button)
char aux_str[128];
char data[10000];
char path[50];
unsigned long previous;

void power_on();
int8_t sendATcommand(const char* ATcommand, const char* expected_answer1, unsigned int timeout);


void setup() {

  pinMode(onModulePin, OUTPUT);
  Serial.begin(115200);

  printf("Starting...\n");
  power_on();

  delay(3000);

  //sets the PIN code
  sprintf(aux_str, "AT+CPIN=%s", sim_pin);
  sendATcommand(aux_str, "OK", 2000);

  delay(3000);

  printf("Connecting to the network...\n");

  while ( (sendATcommand("AT+CREG?", "+CREG: 0,1", 500) ||
           sendATcommand("AT+CREG?", "+CREG: 0,5", 500)) == 0 );

  printf("Succesfully connected to the network\n");

  // sets pop3 server
  sprintf(data, "AT+POP3SRV=\"%s\",\"%s\",\"%s\",%s", server, user_name, password, port);
  sendATcommand(data, "OK", 2000);

  // sets APN, user name and password
  sprintf(aux_str, "AT+CGSOCKCONT=1,\"IP\",\"%s\"", sim_apn);
  sendATcommand(aux_str, "OK", 2000);

  sprintf(aux_str, "AT+CSOCKAUTH=1,1,\"%s\",\"%s\"", sim_user, sim_password);
  sendATcommand(aux_str, "OK", 2000);

  delay(2000);

  // logs into the server
  answer = sendATcommand("AT+POP3IN", "OK", 10000);
  if (answer == 1)
  {
    printf("Logged into the server\n");

    // gets the first email
    answer = sendATcommand("AT+POP3GET=1", "C:/Email/", 10000);
    if (answer == 1)
    {
      counter = 0;
      while (Serial.available() == 0);
      do {
        path[counter] = Serial.read();
        counter++;
        if ((path[counter - 1] == ' ') || (path[counter - 1] == ','))
        {
          counter--;
        }
        while (Serial.available() == 0);
      } while (path[counter - 1] != 0x0D);

      path[counter - 1] = '\0';

      printf("Email folder: %s\n", path);
    }
    else
    {
      printf("Error getting the email\n");
    }
    sendATcommand("AT+POP3OUT", "OK", 10000);
  }

  //Only enter here, if it has entered in the previous "if" before
  if (answer == 1)
  {

    sendATcommand("AT+FSCD=C:/Email", "OK", 2000);
    sprintf(data, "AT+POP3READ=0,\"%s\"", path);


    // Clean the input buffer
    while ( Serial.available() > 0) Serial.read();

    // Send the AT command
    Serial.println(data);

    counter = 0;
    previous = millis();
    answer = 0;
    data[0] = '\0';
    // this loop waits for the answer
    do {

      if (Serial.available() != 0) {
        data[counter] = Serial.read();
        counter++;
        // check if "OK" is in the response of the module
        if (strstr(data, "OK") != NULL)
        {
          answer = 1;
        }

        // check if "ERROR" is in the response of the module
        if (strstr(data, "ERROR") != NULL)
        {
          answer = 2;
        }
      }
      // Waits for the asnwer with time out
    } while ((answer == 0) && ((millis() - previous) < 10000) && (counter < 9999));

    data[counter] = '\0';
    if (answer == 1)
    {
      printf("Email: %s\n", data);
    }
    else if (counter == 511)
    {
      printf("Buffer limit reached!! Data received: %s\n", data);
    }
    else
    {
      printf("Error\n");
      printf("respuesta %s\n", data);
    }


  }

}
void loop() {


}


void power_on() {

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

int main () {
  setup();
  while (1) {
    loop();
  }
  return (0);
}


