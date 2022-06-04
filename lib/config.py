import requests
import threading as thr
from datetime import datetime
import time
import urllib.request
import os
import logging
from pirc522 import RFID
import RPi.GPIO as GPIO
from gpiozero import Buzzer

LOGGING_FILE = "/home/pi/logs/log.log"
PID_FILE_NAME = "/home/pi/assets/pid.txt"