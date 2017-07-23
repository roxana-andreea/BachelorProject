CC=g++
CFLAGS=-lrt -lpthread

all: sms_send gps_standalone gps_s http_get

sms_send: sms_send.cpp
	$(CC) $(CFLAGS) sms_send.cpp arduPi.cpp -o bin/sms_send

gps_standalone: gps_standalone.cpp
	$(CC) $(CFLAGS) gps_standalone.cpp arduPi.cpp -o bin/gps_standalone

gps_s: gps_s.cpp
	$(CC) $(CFLAGS) gps_s.cpp arduPi.cpp -o bin/gps_s

http_get: http_get.cpp
	$(CC) $(CFLAGS) http_get.cpp arduPi.cpp -o bin/http_get

clean:
	rm -f bin/*
