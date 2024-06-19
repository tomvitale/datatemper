#!/usr/bin/env python
# -*- coding: utf-8 -*-
# datatemper.py

# TODO: daily graph | weekly graph | ...

# Copyright (C) 2019  tomvitale
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
	RPi WEb Server for DHT captured data with Graph plot  
'''
# # # # # CUSTOMIZATION # # # # #
desc = "DATATEMPER"
maxSamples = 48
alertTemp = 34
# # # # # # # # # # # # # # # # #

# library
import io
import threading
import time
from datetime import date, timedelta
import os
import seaborn as sns
import sqlite3
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template, send_file, make_response, request

app = Flask(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))
db_path = dir_path + "/datatemper-data.db"

conn = sqlite3.connect(db_path, check_same_thread=False)
curs = conn.cursor()

lock = threading.Lock()

# Retrieve database rows
def numSamples():
	global maxSamples
	todayDate = time.strftime("%Y-%m-%d 00:00:00")
	curs.execute("select COUNT(*) from DHT_day WHERE timestamp > '"+todayDate+"'")
	count = curs.fetchall()
	numSamples = count[0][0]
	if (numSamples > maxSamples):
		numSamples = maxSamples
	return numSamples

# Retrieve database rows Prev
def numSamplesPrev():
	global maxSamples
	todayDate = time.strftime("%Y-%m-%d 00:00:00")
	yesterday = date.today() - timedelta(days=1)
	yesterdayDate = yesterday.strftime("%Y-%m-%d 00:00:00")
	curs.execute("select COUNT(*) from DHT_day WHERE timestamp > '"+yesterdayDate+"' AND timestamp < '"+todayDate+"'")
	count = curs.fetchall()
	numSamples = count[0][0]
	if (numSamples > maxSamples):
		numSamples = maxSamples
	return numSamples

# Retrieve LAST data from database
def getLastData():
	for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
		dates = str(row[0])
		temp = row[1]
		hum = row[2]
	#conn.close()
	return dates, temp, hum

# Retrieve numSamples data from database
def getHistData():
	global maxSamples
	todayDate = time.strftime("%Y-%m-%d 00:00:00")
	curs.execute("SELECT * FROM DHT_day WHERE timestamp > '"+todayDate+"' LIMIT "+str(maxSamples))
	data = curs.fetchall()
	dates = []
	temps = []
	hums = []
	for row in reversed(data):
		dates.append(row[0])
		temps.append(row[1])
		hums.append(row[2])
	return dates, temps, hums

# Retrieve numSamples data from database
def getHistDataPrev():
	global maxSamples
	yesterday = date.today() - timedelta(days=1)
	yesterdayDate = yesterday.strftime("%Y-%m-%d 00:00:00")
	todayDate = time.strftime("%Y-%m-%d 00:00:00")
	curs.execute("SELECT * FROM DHT_day WHERE timestamp > '"+yesterdayDate+"' AND timestamp < '"+todayDate+"' LIMIT "+str(maxSamples))
	data = curs.fetchall()
	dates = []
	temps = []
	hums = []
	for row in reversed(data):
		dates.append(row[0])
		temps.append(row[1])
		hums.append(row[2])
	return dates, temps, hums

# main route 
@app.route("/")
def index():
	dates, temp, hum = getLastData()
	templateData = {
		'dates'		: dates,
		'temp'		: temp,
		'hum'		: hum,
		'desc'		: desc
	}
	return render_template('index.html', **templateData)

@app.route("/realtime.html")
def realtime():
	dates, temp, hum = getLastData()
	templateData = {
		'dates'		: dates,
		'temp'		: temp,
		'hum'		: hum,
		'desc'		: desc
	}
	return render_template('realtime.html', **templateData)

@app.route("/script.html")
def script():
	dates, temp, hum = getLastData()
	templateData = {
		'dates'		: dates,
		'temp'		: temp,
		'hum'		: hum,
		'alert'		: alertTemp
	}
	return render_template('script.html', **templateData)

@app.route('/plot/temperature.png')
def plot_temp():
	lock.acquire(True)
	global alertTemp
	global maxSamples
	dates, temps, hums = getHistData()
	ys = temps
	fig = Figure()
	axes = fig.add_subplot(1, 1, 1)
	axes.set_title("Today Temperature [°C]")
	axes.set_xlabel("Samples: " + str(numSamples()) + " | Alert: " + str(alertTemp) + "°C")
	axes.set_xlim([1,maxSamples])
	axes.set_ylim([1,40])
	axes.hlines(y=alertTemp, xmin=0, xmax=maxSamples, linewidth=1, color='r')
	axes.grid(True)
	xs = range(numSamples())
	axes.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	lock.release()
	return response

@app.route('/plot/temperaturePrev.png')
def plot_tempPrev():
	lock.acquire(True)
	global alertTemp
	global maxSamples
	dates, temps, hums = getHistDataPrev()
	ys = temps
	fig = Figure()
	axes = fig.add_subplot(1, 1, 1)
	axes.set_title("Yesterday Temperature [°C]")
	axes.set_xlabel("Samples: " + str(numSamplesPrev()) + " | Alert: " + str(alertTemp) + "°C")
	axes.set_xlim([1,maxSamples])
	axes.set_ylim([1,40])
	axes.hlines(y=alertTemp, xmin=0, xmax=maxSamples, linewidth=1, color='r')
	axes.grid(True)
	xs = range(numSamplesPrev())
	axes.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	lock.release()
	return response

@app.route('/plot/humidity.png')
def plot_hum():
	lock.acquire(True)
	global maxSamples
	dates, temps, hums = getHistData()
	ys = hums
	fig = Figure()
	axes = fig.add_subplot(1, 1, 1)
	axes.set_title("Today Humidity Rel. [%]")
	axes.set_xlabel("Samples: " + str(numSamples()))
	axes.set_xlim([1,maxSamples])
	axes.set_ylim([1,100])
	axes.grid(True)
	xs = range(numSamples())
	axes.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	lock.release()
	return response

@app.route('/plot/humidityPrev.png')
def plot_humPrev():
	lock.acquire(True)
	global maxSamples
	dates, temps, hums = getHistDataPrev()
	ys = hums
	fig = Figure()
	axes = fig.add_subplot(1, 1, 1)
	axes.set_title("Yesterday Humidity Rel. [%]")
	axes.set_xlabel("Samples: " + str(numSamplesPrev()))
	axes.set_xlim([1,maxSamples])
	axes.set_ylim([1,100])
	axes.grid(True)
	xs = range(numSamplesPrev())
	axes.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	lock.release()
	return response

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=False)
