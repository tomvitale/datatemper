#!/usr/bin/python
# -*- coding: utf-8 -*-

# crontab example
# */5 * * * *     /usr/bin/python3 /opt/projects/datatemper/scripts/mail-alert.py >> /tmp/warningtemp.txt_log
# 0 1 * * *       > /tmp/warningtemp.txt

import csv
import sys
import smtplib, ssl
import urllib.request

fname = "<FILE NAME>" # i.e. /tmp/warningtemp.txt
num_lines = 0

with open(fname, 'r') as f:
    for line in f:
        num_lines += 1

with urllib.request.urlopen('http://<DATATEMPER IP>/script.html') as response:
   html = response.read()
data = html.decode('utf-8').split(',')

#numArg = len(sys.argv)
#temp = str(sys.argv[1])

date = data[0]
temp = data[1]
humr = data[2]
alert = data[3]

if (float(temp) < float(alert) or num_lines >= 3): # if temperature is OK
	print("temperature:"+ temp + " (alert:" + alert  + ") - warning: " + str(num_lines))
else: # altrimenti mando la mail
	port = 25
	smtp_server = "<IP SMTP SERVER>"
	sender_email = "<EMAIL FROM>"
	receiver_email = "<EMAIL TO>" #i.e. "example@example.it, example2@example.it"
	message = """\
Subject: <YOUR SUBJECT> - """ + temp + """C !!

Warning """ + str(num_lines) + """ del """ + date + """

. Temperature: """ + temp + """C
. Umidity Rel.:""" + humr + """ H

link: http://<IP DATATEMPER SERVER>/

(alert Temperature set to """ + str(alert) + """)
"""
	#message.encode('utf-8')
	#message = _fix_eols(message).encode('ascii')
	context = ssl.create_default_context()
	with smtplib.SMTP(smtp_server, port) as server:
	    server.ehlo()  # Can be omitted
	    server.sendmail(sender_email, receiver_email.split(','), message)

	num_lines += 1
	file = open(fname,"a+")
	file.write("Warning "+str(num_lines)+" \n")
	file.close()

	print(message)
