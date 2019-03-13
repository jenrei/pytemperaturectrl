# -*- coding: utf-8 -*-
"""
julabo.py

Contains Julabo temperature control
 see documentation http://www.julabo.com/sites/default/files/downloads/manuals/french/19524837-V2.pdf at section 10.2.
 :copyright: (c) 2015 by Maxime DAUPHIN
 :license: MIT, see LICENSE for details
"""

import serial
import time
from .pytemperaturectrl import TemperatureControl


class Julabo(TemperatureControl):
	"""Julabo Temperature control implementation"""
	
	# see Julabo doc
	MIN_TIME_INTERVAL = 0.250
	
	def __init__(self, *args, **kwargs):
		super(TemperatureControl, self).__init__()
		self.serial = None 
		
	def checkIfOpen(self):
		""" Check if serial port is open """
		if self.serial == None:
			raise Exception("Please call open function before all communication")
		
	def open(self, com_port, baudrate=4800):
		""" Open serial communication"""
		self.serial = serial.Serial(com_port,
				 baudrate=baudrate,
				 bytesize=serial.SEVENBITS,
				 parity=serial.PARITY_EVEN,
				 stopbits=serial.STOPBITS_ONE,
				 timeout=1,
				 xonxoff=False,
				 rtscts=True,
                 dsrdtr=False)

	def close(self):
		""" Close serial communication"""
		self.checkIfOpen()
		if self.serial != None :
			self.serial.close()
			
	def power(self, on):
		"""set power to on or off"""
		self.checkIfOpen()
		time.sleep(self.MIN_TIME_INTERVAL)
		value = 1 if on else 0
		self.serial.write(b'f"out_mode_05 {value}\r\n"')
		
	def getVersion(self):
		"""retrieve engine version"""
		self.checkIfOpen()
		time.sleep(self.MIN_TIME_INTERVAL)
		self.serial.write(b'version\r\n')
		return self.serial.readline()

	def getStatus(self):
		"""retrieve engine status"""
		self.checkIfOpen()
		time.sleep(self.MIN_TIME_INTERVAL)
		self.serial.write(b'status\r\n')
		return self.serial.readline()
		
	def setWorkTemperature(self, temperature_in_degree):
		"""set setpoint temperature"""
		self.checkIfOpen()
		time.sleep(self.MIN_TIME_INTERVAL)
		self.serial.write(b'f"out_sp_00 {temperature_in_degree}\r\n"')

	def getWorkTemperature(self):
		"""get setpoint temperature"""
		self.checkIfOpen()
		time.sleep(self.MIN_TIME_INTERVAL)
		self.serial.write(b'in_sp_00\r\n')
		return float(self.serial.readline())

	def getCurrentTemperature(self):
		"""get current tank temperature"""
		self.checkIfOpen()
		time.sleep(self.MIN_TIME_INTERVAL)
		self.serial.write(b'in_pv_00\r\n')
		return float(self.serial.readline())		
