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
const char port[ ] = "*****";
char server_message[ ] = "*****";

char server_IP[16];

void power_on();
int8_t sendATcommand(const char* ATcommand, const char* expected_answer1, unsigned int timeout);

int8_t client;
int8_t answer;
int onModulePin = 2, aux;
int x;
unsigned long previous;
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

  sprintf(aux_str, "AT+NETOPEN=\"TCP\",%s", port);
  answer = sendATcommand(aux_str, "Network opened", 20000);

  if (answer == 1)
  {
    printf("Network opened\n");
    answer = sendATcommand("AT+SERVERSTART", "OK", 20000);
    if (answer == 1)
    {
      printf("Server started\n");

      sendATcommand("AT+IPADDR", "+IPADDR: ", 20000);

      x = 0;
      do {
        while ( Serial.available() == 0);
        server_IP[x] = Serial.read();
        x++;
      } while (server_IP[x - 1] != 0x0D);
      server_IP[x - 1] != '\0';

      printf("Server IP: %s\n", server_IP);

      do {
        printf("Waiting for clients...\n");

        // Clean the input buffer
        while ( Serial.available() > 0) Serial.read();

        Serial.println("AT+LISTCLIENT");

        x = 0;
        previous = millis();

        client = 0;
        answer = 0;
        // this loop waits for the answer
        do {

          if (Serial.available() != 0) {
            aux_str[x] = Serial.read();
            if (aux_str[x] == 0x0D)
            {
              client++;
            }
            x++;
            if (strstr(aux_str, "OK") != NULL)
            {
              answer = 1;
            }
            if (strstr(aux_str, "ERROR") != NULL)
            {
              answer = 2;
            }
          }
          // Waits for the asnwer with time out
        } while ((answer == 0) && ((millis() - previous) < 10000));

        Serial.println(client, DEC);
        Serial.println(aux_str);
        client -= 2;

        if (client > 0 && (answer == 1))
        {
          printf("Clients connected: %d\n", client);

          for (int y = 0; y < client; y++)
          {
            sprintf(aux_str, "AT+ACTCLIENT=%d", client);
            if (sendATcommand(aux_str, "OK", 10000) == 1)
            {
              sprintf(aux_str, "AT+TCPWRITE=%d", strlen(server_message));
              answer = sendATcommand(aux_str, ">", 20000);
              if (answer == 1)
              {
                sendATcommand(server_message, "Send OK", 20000);
              }
              sprintf(aux_str, "AT+CLOSECLIENT=%d", client);
              sendATcommand(aux_str, "OK", 20000);
            }
          }
        }
        else
        {
          printf("No clients connected\n");
        }
        delay(5000);
      }
      while (client <= 0);

      sendATcommand("AT+NETCLOSE", "OK", 20000);
    }
    else
    {
      printf("Error opening the socket\n");
    }
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


