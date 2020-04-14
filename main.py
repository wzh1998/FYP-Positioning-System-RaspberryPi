# File: main.py
# Author: Zihao Wang, He Wang, Meichen Lu, Jingxiang Sun
# Usage: python3 main.py
#
# Copyright (c) 2020, UCD-FYP Group 12. All Rights Reserved.
# For more information about the authors, goto www.wangzihao.org

import serial
import serial.tools.list_ports
import string
import binascii
import time
import threading
import pymysql
import time

equip_list = []
card_list = []
active_card_list = []

room_location = "Floor 1, Room 101"

def Read_Card_File():
	with open('card_info.txt','r') as f:
		line = f.readline().strip()
		while line:
			print("Card Loading: %s" % line)
			card_list.append(line)
			line = f.readline().strip()

def Read_Equipment_File():
	with open('equipment_info.txt','r') as f:
		line = f.readline().strip()
		while line:
			print("Equipment Loading: %s" % line)
			equip_list.append(line)
			line = f.readline().strip()

def Time_Current():
	currentTime = time.strftime("%Y-%m-%d %H:%M:%S ",time.localtime(time.time()))

	return currentTime

def SQL_Equipment_Update(equipID, location):
	db = pymysql.connect(host="39.108.231.244", user="root", password="logic", database="HETS", charset="utf8")
	# Using cursor() to get operating index
	cursor = db.cursor()

	# Get update time using time function
	updateTime = Time_Current()

	# Construct SQL update statement
	sql = "UPDATE Equipments SET LastUpdateTime='%s', LastLocation='%s' WHERE EquipID = '%s'" % (updateTime, location, equipID)
	
	try:
		# Execute SQL Statement
		cursor.execute(sql)
		# Submit SQL Statement to the Database
		db.commit()
		print("Log: Information of '%s' has been updated successfully on '%s'" % (equipID, location))
	except:
		# Rollback when error happens
		print("Warning: Update failed, please check the network connection.")
		db.rollback()

	# Close SQL connection
	db.close()

	return

def schdule_uploading():
	Read_Equipment_File()
	while(1):
		print("Prepare uploading info to 39.108.231.244 database...")
		for i in range(len(active_card_list)):
			SQL_Equipment_Update(equip_list[active_card_list[i]], room_location)
			time.sleep(1)
		active_card_list.clear()
		time.sleep(10)

def port_list():
	port_list = list(serial.tools.list_ports.comports())
	print(port_list)
	if len(port_list) == 0:
		print('no')
	else:
		for i in range(0,len(port_list)):
			print(port_list[i])
	return

def dynamic_card_list(epc):
	for i in range(len(card_list)):
		if(epc == card_list[i]):
			print("Detected tag with ID: %d" % i)
			if (i not in active_card_list):
				active_card_list.append(i)
			return
	if(epc != None):
		card_list.append(epc)
		print("Found New Tag: %s, added to the system." % epc)
		active_card_list.append(len(card_list)-1)
	return

def set_working_region(ser):
	data = bytes.fromhex('BB 00 07 00 01 01 09 7E')
	result = ser.write(data)
	print("Set working region: China region 2")
	return

def set_working_power(ser):
	data = bytes.fromhex('BB 00 B6 00 02 07 D0 8F 7E')
	result = ser.write(data)
	print("Set working power: 26/20dBm")
	return 

def stop_multi_read(ser):
	data = bytes.fromhex('BB 00 28 00 00 28 7E')
	result = ser.write(data)
	print("Stopping Reading")
	return

def start_multi_read(ser):
	data = bytes.fromhex('BB 00 27 00 03 22 FF FF 4A 7E')
	result = ser.write(data)
	print("Starting multi read: ")
	return

def start_single_read(ser):
	data = bytes.fromhex('BB 00 22 00 00 22 7E')
	result = ser.write(data)
	print("Starting multi read: ")
	return

def get_working_power(ser):
	data = bytes.fromhex('BB 00 B7 00 00 B7 7E')
	ser.write(data)
	print("Get working power")
	return

def set_sensitivity(ser):
	data = bytes.fromhex('BB 00 F5 00 01 00 F6 7E ')
	ser.write(data)
	print("set sensitivity")
	return


def listen_rfid():
	try:
		Read_Card_File()
		

		port_reader = "/dev/ttyUSB0"
		baud_rate = 115200
		time_out = 60

		ser=serial.Serial(port_reader, baud_rate, timeout=time_out)
		print("\ndetailed information about the port:", ser)
			
		# set_working_region(ser)
		# set_working_power(ser)
		set_sensitivity(ser)
		start_multi_read(ser)
		# stop_multi_read(ser)
		while(1):
			if ser.in_waiting:

				htcpl = ser.read(5).hex()
				pl = int(htcpl[6:10], 16)	
				command = int(htcpl[4:6], 16)	
				rest_length = pl+2
				rest_data = ser.read(rest_length).hex()

				if(command == 0x22):
					rssi = int(rest_data[0:2], 16)
					rssi -= 0x100

					epc = rest_data[6:-8]
					dynamic_card_list(epc)

					print("RSSI: %d" % rssi)
				elif(command == 0xFF):
					pass
					# print("No tag has been detected.")
				else:
					print("error, flush current cache")
					ser.flushInput()
					start_multi_read(ser)

	except Exception as e:
		stop_multi_read(ser)
		ser.close()
		print("Exception: ",e)

def main():
	threads = []

	thread1 = threading.Thread(target=listen_rfid)
	threads.append(thread1)

	thread2 = threading.Thread(target=schdule_uploading)
	threads.append(thread2)

	for t in threads:
		t.start()

if __name__ == '__main__':
	main()
	