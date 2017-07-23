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
char url[ ] = "www.google.com";
int port = 443;
char request[ ] = "GET /index.html HTTP/1.1\r\nHost: www.mywebsite.com\r\nContent-Length: 0\r\n\r\n";

const char pin[] = "your_pin";
const char apn[] = "your_apn";
const char user_name[] = "your_user_name";
const char password[] = "your_password";

void power_on();
int8_t sendATcommand(const char* ATcommand, const char* expected_answer1, unsigned int timeout);
int8_t sendATcommand2(const char* ATcommand, const char* expected_answer1, const char* expected_answer2, unsigned int timeout);

int8_t client;
int8_t answer;
int onModulePin = 2, aux;
int x = 0;
char data[250];
unsigned long previous;
int data_size = 0;
int end_file = 0;


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

  // gets the SSL stack
  answer = sendATcommand("AT+CHTTPSSTART", "OK", 5000);
  if (answer == 1)
  {
    // Opens the HTTP session
    sprintf(aux_str, "AT+CHTTPSOPSE=\"%s\",%d", url, port);
    answer = sendATcommand(aux_str, "OK", 30000);
    if (answer == 1)
    {
      // Stores and sends the request
      sprintf(aux_str, "AT+CHTTPSSEND=%d", strlen(request));
      answer = sendATcommand(aux_str, ">", 5000);
      if (answer == 1)
      {
        answer = sendATcommand(request, "OK", 5000);
        if (answer == 1)
        {
          // request the url
          answer = sendATcommand("AT+CHTTPSSEND", "OK", 5000);

          if (answer == 1)
          {
            answer = sendATcommand("AT+CHTTPSRECV=1", "+CHTTPSRECV: DATA,", 60000);

            x = 0;
            do {
              if (answer == 1)
              {
                data_size = 0;
                while (Serial.available() == 0);
                aux = Serial.read();
                do {
                  data_size *= 10;
                  data_size += (aux - 0x30);
                  while (Serial.available() == 0);
                  aux = Serial.read();
                }
                while (aux != 0x0D);

                printf("Data received: %s\n", data_size);

                if (data_size > 0)
                {
                  while (Serial.available() < data_size);
                  Serial.read();

                  for (int y = 0; y < data_size; y++)
                  {
                    data[x] = Serial.read();
                    x++;
                  }
                  data[x] = '\0';
                }
                else
                {
                  printf("Download finished\n");
                }
              }
              else
              {
                printf("Error getting the url\n");
                data_size = 0;
              }

              answer = sendATcommand2("", "+CHTTPSRECV: DATA,", "+CHTTPSRECV:0", 20000);

            }
            while (answer != 1);

            if (answer == 2)
            {
              printf("Data received: %s\n", data);
            }
            else
            {
              printf("Error getting data\n", data);
            }
          }
          else
          {
            printf("Error waiting the request\n", data);
          }
        }
        else
        {
          Serial.println("");
          printf("Error waiting the request\n");
        }

      }
      else
      {
        printf("Error waiting the request\n");
      }
      sendATcommand("AT+CHTTPSCLSE", "OK", 5000);
    }
    else
    {
      printf("Error opening the HTTPS session\n");
    }
    sendATcommand("AT+CHTTPSSTOP", "OK", 5000);
  }
  else
  {
    printf("Error getting the SSL stack\n");
  }

  delay(10000);

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


int8_t sendATcommand2(const char* ATcommand, const char* expected_answer1, const char* expected_answer2, unsigned int timeout)
{

  uint8_t x = 0,  answer = 0;
  char response[100];
  unsigned long previous;

  memset(response, '\0', 100);    // Initialize the string

  delay(100);

  //while( Serial.available() > 0) Serial.read();    // Clean the input buffer

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

