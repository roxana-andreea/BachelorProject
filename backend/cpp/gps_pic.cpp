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

//Write here you SIM card data
const char pin_number[] = "****";
const char apn[] = "*********";
const char user_name[] = "*********";
const char password[] = "*********";

//Write here you server and account data
const char smtp_server[ ] = "*********";      // SMTP server
const char smtp_user_name[ ] = "*********";   // SMTP user name
const char smtp_password[ ] = "*********";    // SMTP password
const char smtp_port[ ] = "***";              // SMTP server port

//Write here your information about sender, direcctions and names
const char sender_address[ ] = "*********";    // Sender address
const char sender_name[ ] = "*********";       // Sender name

const char to_address[ ] = "*********";        // Recipient address
const char to_name[ ] = "*********";           // Recipient name

//Write here the subject and body of the email
char subject[ ] = "GPS+PIC";

int8_t answer, counter;
int onModulePin = 2;    // the pin to switch on the module (without press on button)
char aux_str[1280];
char picture_name[25];
int GPS_retries;
char gps_data[100];

void power_on();
int8_t sendATcommand(const char* ATcommand, const char* expected_answer1, unsigned int timeout);
int8_t sendATcommand2(const char* ATcommand, const char* expected_answer1, const char* expected_answer2, unsigned int timeout);
void get_GPS();
void take_picture();
void send_email();


void setup() {

  pinMode(onModulePin, OUTPUT);
  Serial.begin(115200);

  printf("Starting...\n");
  power_on();

  delay(3000);

  //Use this command if you want to delete the files in C:
  //sendATcommand("AT+FSDEL=*.*", "OK", 3000);

  get_GPS();       // Waits for GPS data
  take_picture();  // Takes a picture
  send_email();    // Sends an email with coordinates and picture
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

void get_GPS() {
  // starts GPS session in stand alone mode
  answer = sendATcommand("AT+CGPS=1,1", "OK", 1000);
  if (answer == 0)
  {
    printf("Error starting the GPS. The code stucks here!!\n");
    while (1);
  }

  GPS_retries = 50;
  do {
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
      gps_data[counter - 1] = '\0';
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
    delay(1000);
    GPS_retries--;
  } while ((GPS_retries > 0) && (gps_data[0] == ','));



  delay(5000);

}


void take_picture() {
  // Starts the camera
  answer = sendATcommand2("AT+CCAMS", "OK", "CAMERA NO SENSOR", 3000);
  if (answer == 1)
  {
    // Sets resolution (Old camera)
    //sendATcommand2("AT+CCAMSETD=640,480", "OK", "ERROR", 2000);

    // Sets resolution (New camera)
    sendATcommand2("AT+CCAMSETD=1600,1200", "OK", "ERROR", 2000);

    printf("Taking photo...\n");
    // Takes a picture, but not saved it
    answer = sendATcommand2("AT+CCAMTP", "OK", "ERROR", 5000);
    delay(1000);
    if (answer == 1)
    {
      // Saves the picture into C:/Picture
      answer = sendATcommand2("AT+CCAMEP", "C:/Picture/", "ERROR", 2000);

      if (answer == 1)
      {
        memset(picture_name, 0x00, sizeof(picture_name));
        counter = 0;
        while (Serial.available() == 0);
        do {
          picture_name[counter] = Serial.read();
          counter++;
          while (Serial.available() == 0);
        } while (picture_name[counter - 1] != 0x0D);

        picture_name[counter - 1] = '\0';

        printf("Picture name: %s\n", picture_name);

        sendATcommand2("AT+CCAME", "OK", "OK", 2000);

      }
      else
      {

        printf("Error saving the picture\n");
      }
    }
    else if (answer == 2)
    {
      printf("Camera invalid state\n");
    }
    else
    {
      printf("Error taking the picture\n");
    }
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

void send_email() {
  //sets the PIN code
  sprintf(aux_str, "AT+CPIN=%s", pin_number);
  sendATcommand(aux_str, "OK", 2000);

  delay(3000);

  while ( (sendATcommand("AT+CREG?", "+CREG: 0,1", 500) ||
           sendATcommand("AT+CREG?", "+CREG: 0,5", 500)) == 0 );

  // sets the SMTP server and port
  sprintf(aux_str, "AT+SMTPSRV=\"%s\",%s", smtp_server, smtp_port);
  sendATcommand(aux_str, "OK", 2000);

  // sets user name and password
  sprintf(aux_str, "AT+SMTPAUTH=1,\"%s\",\"%s\"", smtp_user_name, smtp_password);
  sendATcommand(aux_str, "OK", 2000);

  // sets sender adress and name
  sprintf(aux_str, "AT+SMTPFROM=\"%s\",\"%s\"", sender_address, sender_name);
  sendATcommand(aux_str, "OK", 2000);

  // sets sender adress and name
  sprintf(aux_str, "AT+SMTPRCPT=1,0,\"%s\",\"%s\"", to_address, to_name);
  sendATcommand(aux_str, "OK", 2000);

  // subjet of the email
  sprintf(aux_str, "AT+SMTPSUB=\"%s\"", subject);
  sendATcommand(aux_str, "OK", 2000);

  // body of the email
  sprintf(aux_str, "AT+SMTPBODY=\"%s\"", gps_data);
  sendATcommand(aux_str, "OK", 2000);

  //It's normal to receive an error in this instruction if you are already in this folder
  sendATcommand("AT+FSCD=Picture", "OK", 2000);

  sprintf(aux_str, "AT+SMTPFILE=1,\"%s\"", picture_name);
  sendATcommand(aux_str, "OK", 2000);

  // sets APN, user name and password
  sprintf(aux_str, "AT+CGSOCKCONT=1,\"IP\",\"%s\"", apn);
  sendATcommand(aux_str, "OK", 2000);

  sprintf(aux_str, "AT+CSOCKAUTH=1,1,\"%s\",\"%s\"", user_name, password);
  sendATcommand(aux_str, "OK", 2000);

  delay(1000);

  printf("Sending email...\n");

  // sends the email and waits the answer of the module
  answer = sendATcommand("AT+SMTPSEND", "+SMTP: SUCCESS", 60000);
  if (answer == 1)
  {
    printf("Done!\n");
  }
  else
  {
    printf("Error\n");
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



