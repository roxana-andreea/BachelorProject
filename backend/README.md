# Backend Documentation

## OBD SIM
> bcdedit.exe -set TESTSIGNING ON
> .\com2tcp-rfc2217.bat --rfc2217-mode s \\.\CNCB0 5544

> (Pdb) tn.write(b'01 00\r\n')
> b'01 00\r\n\r\n41 00 88 19 80 00\r\n>'
> 1000 1000 0001 1001 1000 0000 0000 0000
> 01 05 12 13 16 17
## VSS Installation Procedure
> apt-get install ansible git
> mv /etc/ansible /etc/ansible.bk
> ln -s /root/backend/ansible /etc/ansible
> TODO: mysql_install_db
> TODO: mysql_secure_installation
> TODO: add .my.cnf
> TODO: php5enmod mcrypt
> apt-get install python-django

### A-GPS

AT+CREG?

AT+CGSOCKCONT=1,\"internet\"
AT+CGPSURL=\"supl.google.com:7276\"
AT+CGPSSSL=0  
AT+CGPS=1,2
AT+CGPSINFO
AT+CGPSSWITCH


###Gammu SMSD Testing

>root@rpi3:~# sudo /usr/local/sbin/sms_receive.py IN20160618_233927_00_+40753174860_00.txt
filename=IN20160618_233927_00_+40753174860_00.txt
dirname=/var/spool/gammu/inbox/
Received SMS from number: '+40753174860' with text: 'Test6'

##Python Serial
>root@rpi:~/backend/cpp/bin# python -m serial.tools.list_ports
/dev/ttyUSB0
/dev/ttyUSB1
/dev/ttyUSB2
/dev/ttyUSB3
/dev/ttyUSB4
5 ports found

## Django

>python manage.py migrate, check
>python manage.py makemigrations 
> sqlmigrate polls 0001

## USB2CAN
>rpi-update
>reboot
>sudo wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/bin/rpi-source && sudo chmod +x /usr/bin/rpi-source && /usr/bin/rpi-source -q --tag-update
>apt-get install bc libncurses5-dev dkms
>cd /root ; git clone https://github.com/krumboeck/usb2can.git
>cd /root/usb2can ; git archive --prefix=usb2can-1.0/ -o /usr/src/usb2can-1.0.tar HEAD
>cd /usr/src; tar xvf usb2can-1.0.tar
>cd /usr/src/usb2can-1.0/
>dkms add -m usb2can -v 1.0 --verbose
>dkms build -m usb2can -v 1.0 --verbose
>dkms install -m usb2can -v 1.0 --verbose
>modprobe can_raw
>modprobe can_dev
>insmod /lib/modules/4.4.10-v7+/extra/usb_8dev.ko
>ip link set can0 up type can bitrate 1000000 sample-point 0.875

## Flask

Tools to install: Flask + Jinja2 + Peewee

## RPI Installation Procedure
### Install OS
Follow NOOBS instructions

### Update OS

>rpi-update
>raspi-config
>apt-get update
>apt-get dist-upgrade

### Configuration Management

> apt-get install ansible 

### Firewall

> ufw allow ssh
> ufw enable

### Web Server

> a2enmod cgi

>cat /etc/apache2/conf-enabled/serve-cgi-bin.conf
><Directory "/usr/lib/cgi-bin">
>...
>AddHandler cgi-script .py
>...
></Directory>

> chmod a+rx /usr/lib/cgi-bin/*
> service apache2 restart

### Sensors

 * Wiring PI
 * I2C
 * SPI

### Serial

 * python-serial
 * python-usb
 * wvdial
 * setserial
 * ardupi

> wget http://www.cooking-hacks.com/media/cooking/images/documentation/raspberry_arduino_shield/raspberrypi2.zip && unzip raspberrypi2.zip && cd raspberrypi_2.0 && chmod +x compile_rpi2 && ./compile_rpi2 && cd ..


### Modem
Configure settings:
> - Speed (baud rate): 115200
> - Bits: 8
> - Parity: None
> - Stop Bits: 1
> - Flow Control: None

### APN

#### Orange
> User name: "Internet"
Password: "Orange"
APN (Access Point Name): "internet"
number call: *99# or *99***1# (depending on the telephone type)
proxy server: 172.22.7.20
port: 80
user name: blank
password: blank
modem initialization commands:
at+cgdcont=1,”ip”,”internet”,””,0,0
at+cgdcont=1,”ip”,”internet”

#### SMS
> apt-get install gammu


### AP WiFI 

Configure AP settings

> iwlist wlan0 scan

### Remote Shares

> mount -o uid=pi,user=XXX,password=XXX //10.5.0.4/serials /media/serials


##  Commands 
### AT Disable PIN
Disable pin code:

> AT+CPIN?
 +CPIN: SIM PIN // pin codes need to be entered
 OK
>
AT+CPIN="9546"
 OK
>
AT+CLCK="SC",0,"9546" // disable pin code
 OK
>
AT+CPIN?
 +CPIN: READY

### S-GPS

>+CGPSINFO: [<latitude>],[<N/S>],[<longitude>],[<E/W>],[<date>],[<UTC_time>],[<altitude>],[<speedOG>],[<course>]

> AT+CGPSINFO
> +CGPSINFO:4426.788279,N,02603.527478,E,210316,191016.1,-13.0,0,0
+CGPSINFO:4426.785259,N,02603.531758,E,210316,191057.0,39.5,0,0
+CGPSINFO:4426.785251,N,02603.531763,E,210316,191101.0,39.0,0,0
+CGPSINFO:4426.772309,N,02603.549073,E,210316,191731.0,111.0,0,0
+CGPSINFO:4426.768046,N,02603.564689,E,210316,192717.0,105.5,0,0

>Degrees and decimal minutes (DMM): 44°26'76.8046"N 2°603'531758.5"E

### TTY baud rate
> stty -F /dev/ttyUSB0 9600
$ stty -F /dev/ttyUSB0 -a
speed 0 baud; rows 0; columns 0; line = 0;

> modprobe usbserial vendor=0x0403 product=0xfa24

Add line in /etc/modules 
> usbserial vendor=0x0403 product=0xfa24

### System Information

>cat /sys/block/mmcblk0/device/cid  
035344534c33324780b160118d00fb89  
grep Serial /proc/cpuinfo | cut -d ":" -f2 | sed -e "s/^ *//g"
00000000b1b69e35
ifconfig eth0 | grep HWaddr | cut -d " " -f11 | sed -e "s/://g"
b827ebb69e35

## Functional Description

### REMOTE CONTROLS
 * Door Lock/Unlock
 * Engine Start/Stop
 * Window Up/Down
 * Engine Shutdown/Disable
### SECURITY, TRACKING, AND ALERTS GPS
 * Location Tracking
 * Alarm Siren Monitor
 * Towing/Bump Alerts
 * Low Battery Alerts
 * Virtual Security Zone/Geofence Alert
 * Vehicle Overspeed Alert
 * Vehicle Engine On/Off Monitor
 * SOS Emergency Switch.
 * Door Entry Sensor
 * Built-In 72hr back-up Battery
 * Unit unplugged Alert
### COMPATIBILITY
 * Unlimited Range
 * Share Alerts via Text and Email
 * Works For All Cars
 * Compatible With Any Existing Alarm/Factory Alarm System
 * View Multiple Cars From One Phone
 * Compatible With Multiple Users
 * Works In All Countries (GSM Coverage)
 * Installation Required
 * Read Engine Diagnostics
 * Works for Motorcycles
 * Web Control
 * Text Control
 * App Control

## Logs

### Ross Tech USB ###

> #dmesg
[ 5330.598527] usb 2-2.2: new full-speed USB device number 5 using uhci_hcd
[ 5330.715534] usb 2-2.2: New USB device found, idVendor=0403, idProduct=fa24
[ 5330.715538] usb 2-2.2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[ 5330.716660] usb 2-2.2: Product: Ross-Tech HEX-USB
[ 5330.716766] usb 2-2.2: Manufacturer: Ross-Tech
[ 5330.716768] usb 2-2.2: SerialNumber: RT000001
 # lsusb
Bus 002 Device 005: ID 0403:fa24 Future Technology Devices International, Ltd 

>[   92.903357] usbcore: registered new interface driver usbserial
[   92.903576] usbcore: registered new interface driver usbserial_generic
[   92.903801] usbserial: USB Serial support registered for generic
[   92.922635] usbcore: registered new interface driver option
[   92.922798] usbserial: USB Serial support registered for GSM modem (1-port)
[   97.325109] usb 1-1.5: new high-speed USB device number 18 using dwc_otg
[   97.427443] usb 1-1.5: New USB device found, idVendor=05c6, idProduct=9000
[   97.427471] usb 1-1.5: New USB device strings: Mfr=3, Product=2, SerialNumber=0
[   97.427488] usb 1-1.5: Product: SimTech SIM5218
[   97.427503] usb 1-1.5: Manufacturer: SimTech, Incorporated

### ELM 327
> AT Z (reset)
> AT SP 0 (select comm protocol 0)
> 01 00 (expect answer with supported PIDs 41 00 XX XX XX XX)
> 01 05 (temp, answer 41 05 7B, 7B = temp in hexa, convert in dec, substract 40)
> 01 0C (engine rpm, 41 0C 1A F8, divide by 4)


>AT Z
>LM327 v1.5
>AT SP 0
>K SP 0
>K
>K
>01 05
>1 05 78 ...
>1 05 78
>01 0C78
>01 0C00 00
>AT Z 00 00
>LM327 v1.5
>
>
>AT SP 0
>K SP 0
>K
>K
>K
>K
>K
>01 05
>01 0C78 ...
>1 0C 0D 18
>1 0C 0D 1C
>1 0C 16 DC
>1 0C 0C 60
>1 0C 20 00
>1 0C 28 94
>1 0C 26 98
>1 0C 1C EC

### Bluetooth

>root@rpi:~# hcitool scan
Scanning ...
    10:41:7F:A8:5C:F7   Cristian's iPhone
root@rpi:~# sdptool search SP
Inquiring ...
Searching for SP on 10:41:7F:A8:5C:F7 ...
Service Name: Wireless iAP
Service RecHandle: 0x4f4907e0
Service Class ID List:
  UUID 128: 00000000-deca-fade-deca-deafdecacafe
Protocol Descriptor List:
  "L2CAP" (0x0100)
  "RFCOMM" (0x0003)
    Channel: 1
Language Base Attr List:
  code_ISO639: 0x656e
  encoding:    0x6a
  base_offset: 0x100
  code_ISO639: 0x6672
  encoding:    0x6a
  base_offset: 0x110
  code_ISO639: 0x6465
  encoding:    0x6a
  base_offset: 0x120
  code_ISO639: 0x6a61
  encoding:    0x6a
  base_offset: 0x130
Profile Descriptor List:
  "Serial Port" (0x1101)
    Version: 0x0100

root@rpi:~# rfcomm connect 0 10:41:7F:A8:5C:F7 1
Connected /dev/rfcomm0 to 10:41:7F:A8:5C:F7 on channel 1
Press CTRL-C for hangup
^CDisconnected

root@rpi:~# bluetoothctl
[NEW] Controller 00:1A:7D:DA:71:13 rpi [default]
[bluetooth]# power on
Changing power on succeeded
[bluetooth]# scan on
Discovery started
[CHG] Controller 00:1A:7D:DA:71:13 Discovering: yes
[NEW] Device 10:41:7F:A8:5C:F7 10-41-7F-A8-5C-F7
[CHG] Device 10:41:7F:A8:5C:F7 RSSI: -65
[CHG] Device 10:41:7F:A8:5C:F7 Name: Cristian's iPhone
[CHG] Device 10:41:7F:A8:5C:F7 Alias: Cristian's iPhone
[CHG] Device 10:41:7F:A8:5C:F7 UUIDs:
    00001200-0000-1000-8000-00805f9b34fb
    0000111f-0000-1000-8000-00805f9b34fb
    0000112f-0000-1000-8000-00805f9b34fb
    0000110a-0000-1000-8000-00805f9b34fb
    0000110c-0000-1000-8000-00805f9b34fb
    00001116-0000-1000-8000-00805f9b34fb
    00001132-0000-1000-8000-00805f9b34fb
    00000000-deca-fade-deca-deafdecacafe
    2d8d2466-e14d-451c-88bc-7301abea291a
[CHG] Device 10:41:7F:A8:5C:F7 RSSI: -76
[CHG] Device 10:41:7F:A8:5C:F7 RSSI: -68
[CHG] Device 10:41:7F:A8:5C:F7 RSSI: -42
[NEW] Device 60:4B:AB:A4:C4:36 60-4B-AB-A4-C4-36
[CHG] Device 60:4B:AB:A4:C4:36 RSSI: -69
[CHG] Device 60:4B:AB:A4:C4:36 RSSI: -60
[CHG] Device 60:4B:AB:A4:C4:36 RSSI: -68
[CHG] Device 10:41:7F:A8:5C:F7 RSSI: -70
[CHG] Device 10:41:7F:A8:5C:F7 RSSI: -79
[bluetooth]# pair 10:41:7F:A8:5C:F7
Attempting to pair with 10:41:7F:A8:5C:F7
[CHG] Device 10:41:7F:A8:5C:F7 Connected: yes
[CHG] Device 10:41:7F:A8:5C:F7 Modalias: bluetooth:v004Cp6E00d0930
[CHG] Device 10:41:7F:A8:5C:F7 UUIDs:
    00000000-deca-fade-deca-deafdecacafe
    00001000-0000-1000-8000-00805f9b34fb
    0000110a-0000-1000-8000-00805f9b34fb
    0000110c-0000-1000-8000-00805f9b34fb
    0000110e-0000-1000-8000-00805f9b34fb
    00001116-0000-1000-8000-00805f9b34fb
    0000111f-0000-1000-8000-00805f9b34fb
    0000112f-0000-1000-8000-00805f9b34fb
    00001132-0000-1000-8000-00805f9b34fb
    00001200-0000-1000-8000-00805f9b34fb
[CHG] Device 10:41:7F:A8:5C:F7 Paired: yes
Pairing successful
[CHG] Device 10:41:7F:A8:5C:F7 Connected: no
[bluetooth]# pair 10:41:7F:A8:5C:F7
Attempting to pair with 10:41:7F:A8:5C:F7
Failed to pair: org.bluez.Error.AlreadyExists
[CHG] Device 10:41:7F:A8:5C:F7 RSSI: -62
[CHG] Device 10:41:7F:A8:5C:F7 RSSI: -83
[CHG] Device 10:41:7F:A8:5C:F7 RSSI: -74
[bluetooth]# pair 10:41:7F:A8:5C:F7
Attempting to pair with 10:41:7F:A8:5C:F7
Failed to pair: org.bluez.Error.AlreadyExists
[CHG] Device 10:41:7F:A8:5C:F7 Connected: yes
[CHG] Device 10:41:7F:A8:5C:F7 Connected: no
[CHG] Device 10:41:7F:A8:5C:F7 RSSI: -96
[CHG] Device 10:41:7F:A8:5C:F7 RSSI: -65
[CHG] Device 10:41:7F:A8:5C:F7 Connected: yes
[CHG] Device 10:41:7F:A8:5C:F7 Connected: no
[CHG] Device 60:4B:AB:A4:C4:36 RSSI: -60

### ddclient

> ddclient -daemon=0 -debug -verbose -noquiet
> ddclient status

### udev

> udevadm info -a -n /dev/ttyUSB3 | grep '{serial}' | head -n1
    ATTRS{serial}=="3f980000.usb"

### Reverse SSH

> ssh -fN -R 3333:localhost:22 root@vss.no-ip.org -v

### USB Monitoring

>root@rpi:~# dumpcap -D
1. eth0
2. tun0
3. any
4. lo (Loopback)
5. wlan0
6. bluetooth0
7. nflog
8. nfqueue
9. usbmon1

### Gammu

>gammu sendsms TEXT 0751010821 -text "This is a text"
>gammu getallmemory MC
>gammu monitor 1
>gammu getnetworks Romania
>gammu network info
>gammu getallsms -pbk
>root@rpi:~# gammu identify

 ## References 

 [http://weworkweplay.com/play/getting-gps-location-and-transmit-over-3g-edge-gsm-with-arduino-or-raspberry-pi/](A-GPS how-to)
