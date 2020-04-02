import serial
import serial.tools.list_ports
import string
import binascii
import time

def port_list():
	port_list = list(serial.tools.list_ports.comports())
	print(port_list)
	if len(port_list) == 0:
		print('no')
	else:
		for i in range(0,len(port_list)):
			print(port_list[i])

# def query_start() {
	
# }
def set_working_region(ser):
	data = bytes.fromhex('BB 00 07 00 01 01 09 7E')
	result = ser.write(data)
	print("Set working region: China region 2")
	# ser.flushInput()
def set_working_power(ser):
	data = bytes.fromhex('BB 00 B6 00 02 07 D0 8F 7E')
	result = ser.write(data)
	print("Set working power: 26/20dBm")
	# ser.flushInput()

def stop_multi_read(ser):
	data = bytes.fromhex('BB 00 28 00 00 28 7E')
	result = ser.write(data)#BB 00 27 00 03 22 27 10 83 7E
	print("Stopping Reading")
	print("Terminate-")
	# print(ser.read(ser.in_waiting.hex()))

def start_multi_read(ser):
	data = bytes.fromhex('BB 00 27 00 03 22 FF FF 4A 7E')
	result = ser.write(data)
	print("Starting multi read: ")
	# ser.flushInput()

def start_single_read(ser):
	data = bytes.fromhex('BB 00 22 00 00 22 7E')
	result = ser.write(data)#BB 00 27 00 03 22 27 10 83 7E
	print("Starting multi read: ")
	# ser.flushInput()
def get_working_power(ser):
	data = bytes.fromhex('BB 00 B7 00 00 B7 7E')
	ser.write(data)
	print("Get working power")
	# print(ser.read(50).hex())
	# ser.flushInput()

if __name__ == '__main__':
	try:
		port_reader = "/dev/ttyUSB0"
		baud_rate = 115200
		time_out = 60

		ser=serial.Serial(port_reader, baud_rate, timeout=time_out)
		print("\ndetailed information about the port:", ser)
		
		
		set_working_region(ser)
		set_working_power(ser)
		# set_working_power(ser)

		

		start_multi_read(ser)
		ser.flushInput()
		# get_working_power(ser)

		while(1):
			if ser.in_waiting:

				htcpl = ser.read(5).hex()
			
				pl = int(htcpl[6:10], 16)

				print(htcpl)
		
				command = int(htcpl[4:6], 16)
			
				rest_length = pl+2
				rest_data = ser.read(rest_length).hex()
				print(rest_data)
				if(command == 0x22):
					rssi = int(rest_data[0:2], 16)
					# print("Tag detected, rssi: %x" % rssi)
					rssi = ~(0xFF^rssi)
					print("Tag detected, rssi: %d" % rssi)
				elif(command == 0xFF):
					print("No tag detected.")
				else:
					print("error, flush current cache")
					ser.flushInput()

	except Exception as e:
		ser.close()
		stop_multi_read(ser)
		print("Exception: ",e)

