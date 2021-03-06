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

//Change here your data
const char pin[] = "*******";
const char apn[] = "*******";
const char user_name[] = "*******";
const char password[] = "*******";
const char TCP_server_1[ ] = "*******";
const char TCP_port_1[ ] = "*******";
char TCP_message_1[ ] = "*******";
const char TCP_server_2[ ] = "*******";
const char TCP_port_2[ ] = "*******";
char TCP_message_2[ ] = "*******";

void power_on();
int8_t sendATcommand(const char* ATcommand, const char* expected_answer1, unsigned int timeout);

int8_t answer;
int onModulePin = 2, aux;

char aux_str[1000];



void setup() {

  pinMode(onModulePin, OUTPUT);
  Serial.begin(115200);

  printf("Starting...\n");
  power_on();

  delay(3000);

  //sets the PIN code
  snprintf(aux_str, sizeof(aux_str), "AT+CPIN=%s", pin);
  sendATcommand(aux_str, "OK", 2000);

  delay(3000);
  printf("Connecting to the network\n");

  while ( (sendATcommand("AT+CREG?", "+CREG: 0,1", 500) ||
           sendATcommand("AT+CREG?", "+CREG: 0,5", 500)) == 0 );

  printf("Succesfully connected to the network\n");

  // sets APN, user name and password
  snprintf(aux_str, sizeof(aux_str), "AT+CGSOCKCONT=1,\"IP\",\"%s\"", apn);
  sendATcommand(aux_str, "OK", 2000);

  snprintf(aux_str, sizeof(aux_str), "AT+CSOCKAUTH=1,1,\"%s\",\"%s\"", user_name, password);
  sendATcommand(aux_str, "OK", 2000);
}

void loop() {
  sprintf(aux_str, "AT+NETOPEN=,,1");
  answer = sendATcommand(aux_str, "Network opened", 20000);

  if (answer == 1)
  {
    printf("Network opened\n");
    printf("Opening client 1\n");

    sprintf(aux_str, "AT+CIPOPEN=0,\"TCP\",\"%s\",%s", TCP_server_1, TCP_port_1);
    answer = sendATcommand(aux_str, "OK", 20000);
    if (answer == 1)
    {
      printf("Client 1 opened\n");
      sprintf(aux_str, "AT+CIPSEND=0,%d", strlen(TCP_message_1));
      answer = sendATcommand(aux_str, ">", 20000);
      if (answer == 1)
      {
        sendATcommand(TCP_message_1, "OK", 20000);
      }
    }
    sendATcommand("AT+CIPCLOSE=0", "OK", 20000);

    printf("Opening client 2\n");

    sprintf(aux_str, "AT+CIPOPEN=1,\"TCP\",\"%s\",%s",
            TCP_server_2, TCP_port_2);
    answer = sendATcommand(aux_str, "OK", 20000);
    if (answer == 1)
    {
      printf("Client 2 opened\n");
      sprintf(aux_str, "AT+CIPSEND=1,%d", strlen(TCP_message_2));
      answer = sendATcommand(aux_str, ">", 20000);
      if (answer == 1)
      {
        sendATcommand(TCP_message_2, "OK", 20000);
      }
    }
    sendATcommand("AT+CIPCLOSE=1", "OK", 20000);
  }
  else
  {
    printf("Error opening the network\n");
  }

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

int main () {
  setup();
  while (1) {
    loop();
  }
  return (0);
}


