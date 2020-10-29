#!/usr/bin/env python
# -*- coding: utf-8 -*-
# datatemper-log.py

# TODO: optimize code | ...

# Copyright (C) 2020  tomvitale
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>

'''
	RPi DHT data log with Adafruit_DHT into Sqlite3 db  
'''

import Adafruit_DHT
import RPi.GPIO as GPIO
import sqlite3
import sys
import time
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
db_path = dir_path + "/datatemper-data.db"

sampleFreq = 1*60 # time in seconds ==> Sample each 1 min

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.HIGH)

time.sleep(2)

# get data from DHT sensor
def getDHTdata():
	DHT22Sensor = Adafruit_DHT.DHT22
	DHTpin = 20
	hum, temp = Adafruit_DHT.read_retry(DHT22Sensor, DHTpin)
	if hum is not None and temp is not None:
		hum = round(hum)
		temp = round(temp, 1)
	return temp, hum

# log sensor data on database
def logData (temp, hum):
	date = time.strftime("%Y-%m-%d %H:%M:%S")
	conn=sqlite3.connect(db_path)
	curs=conn.cursor()
	curs.execute("INSERT INTO DHT_data values((?), (?), (?))", (date, temp, hum))
	conn.commit()
	conn.close()

# main function
def main():
	while True:
		temp, hum = getDHTdata()
		logData (temp, hum)
		time.sleep(sampleFreq)

# ------------ Execute program 
main()
