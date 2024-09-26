# RFID reader with a Raspberry Pi

## Scope

This project was created for a school project, the goal was to create a **totem** for school attendance that would check if the student was present on the database and would therefore register everyone's entries and exits.

## Result

The code published on this repository allows the creation of an attendance control system, this manages errors related to the internet connection mainly, it is structured so that the raspberry cannot be used for other purposes, to avoid compromises by unauthorized personnel.
We have built and tested everything we have written (and built) obtaining a good result.

## Functioning
The operation is very simple, the raspberry pi is always waiting for an RFID tag, when this is passed a request is forwarded to our webAPI which checks the authenticity of the scanned UID.
An audible and visual signal will signal the success or failure of the reading
The daemon script will be used to restart the reading process in case it is interrupted or stopped in any way.
This file must be inserted in the raspberry *.bashrc* file in order to be started automatically at each start, the script can start the program autonomously for reading.

## Technology Used
We used:
 - Raspberry Pi 3
 - RC522 RFID sensor
 - couple of LEDs
 - 3D printed box

## Credit
This project was developed with the help of:
 - [Michele Alladio](https://github.com/MicheleAlladioAKAMich)
 - [Samuele Forneris](https://github.com/samu4ne)


