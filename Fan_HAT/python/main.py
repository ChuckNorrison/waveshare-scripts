#!/usr/bin/python
# -*- coding:utf-8 -*-

import SSD1306
import PCA9685
import time
import traceback
import socket
import threading
import os
import logging
from PIL import Image,ImageDraw,ImageFont
from systemd.journal import JournalHandler

log = logging.getLogger('fan-hat')
log.addHandler(JournalHandler())
log.setLevel(logging.INFO)
log.info("Start Waveshare Fan_HAT script modified by zed")

# tweak here
temp_target = 48
temp_threshold = 4
interval_sec = 10

# do not change
temp_old = 0
fan_pulse = 0
fan_steps = 10

try:
	oled = SSD1306.SSD1306()

	pwm = PCA9685.PCA9685(0x40, debug=False)
	pwm.setPWMFreq(50)
	pwm.setServoPulse(0,0)
	log.info("Fan off")
	
	# Initialize library.
	oled.Init()
	oled.ClearBlack()

	# Create blank image for drawing.
	image1 = Image.new('1', (oled.width, oled.height), "WHITE")
	draw = ImageDraw.Draw(image1)
	font = ImageFont.load_default()


	while(1):
		draw.rectangle((0,0,128,32), fill = 1)

		# get ip (bad google solution here)
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(('8.8.8.8', 80))
		localhost = s.getsockname()[0]

		#log and update screen
		print("ip:%s" %localhost)
		log.info("ip:%s" %localhost)
		draw.text((0,0), localhost, font=font, fill = 0)

		# get temp
		file = open("/sys/class/thermal/thermal_zone0/temp")  
		temp = float(file.read()) / 1000.00  
		temp = float('%.2f' % temp)
		strTemp = str(temp) + " °C"
		file.close()

		#log and update screen
		print("temp : %.2f" %temp)
		log.info("temp : %.2f" %temp)
		draw.text((0,16), strTemp, font=font, fill = 0)
		
		# check temps and set fan pulse
		if temp_old == 0:
			temp_old = temp
		else:
			# high temp
			if temp > temp_target + temp_threshold:
				if fan_pulse == 0:
					fan_pulse = fan_steps
				else:
					if temp > temp_old:
						# increase fan speed if temp goes up
						fan_pulse = fan_pulse + fan_steps
					elif temp < temp_old:
						# decrease fan speed if temp goes down
						if fan_pulse > fan_steps:
							fan_pulse = fan_pulse - fan_steps

				# limit fan speed to 80% max speed
				if fan_pulse > 80:
					fan_pulse = 80

				pwm.setServoPulse(0,fan_pulse)
				log.info("Fan %d%%" % fan_pulse)
			# default temp
			elif temp > temp_target:
				# default to min speed
				fan_pulse = fan_steps
				pwm.setServoPulse(0,fan_pulse)
				log.info("Fan %d%%" % fan_pulse)
			# good temp
			elif temp < temp_target:
				pwm.setServoPulse(0,0)
				log.info("Fan off")

		#show
		oled.ShowImage(oled.getbuffer(image1.rotate(180)))
		time.sleep(interval_sec)

except IOError as e:
    oled.Closebus()
    print(e)
    log.error(str(e))
    
except KeyboardInterrupt:    
    print("ctrl + c:")
    oled.Closebus()
    