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
def stop_multi_read(ser):
	data = bytes.fromhex('BB 00 28 00 00 28 7E')
	result = ser.write(data)#BB 00 27 00 03 22 27 10 83 7E
	print("\nStopping Reading",result)
	print("\nStop result: ")
	print(ser.read().hex())

def start_multi_read(ser):
	data = bytes.fromhex('BB 00 27 00 03 22 FF FF 4A 7E')
	result = ser.write(data)#BB 00 27 00 03 22 27 10 83 7E
	print("Starting multi read: ", result)

def start_single_read(ser):
	data = bytes.fromhex('BB 00 22 00 00 22 7E')
	result = ser.write(data)#BB 00 27 00 03 22 27 10 83 7E
	print("Starting multi read: ", result)

if __name__ == '__main__':
	try:
		port_reader = "/dev/ttyUSB0"
		baud_rate = 115200
		time_out = 60

		ser=serial.Serial(port_reader, baud_rate, timeout=time_out)
		print("\ndetailed information about the port:", ser)
		# write
		
		# print(ser.read().hex())
		# read
		start_multi_read(ser)
		# stop_multi_read(ser)
		
		while(1):
			if ser.in_waiting:

				# print(ser.in_waiting)
				# Get header, type, command
				# htcpl = ser.read(5).hex()
				htcpl = ser.read(5).hex()
				# command = htc[2:-2];
				# if(len(response_msg)==16):
					# print("no tag detected")
				# elif(len(response_msg)>16):
					# print("tt")

				pl = int(htcpl[6:10], 16)
				print(htcpl)
				
				print("%d" % pl)
				# print()
				
				# get parameter 
				# parameter = str1[12:14]

				# if((parameter == "15")):
				# 	print("no tag detected")
				# else:
				# 	print(str1)
				# 	print("\n", len(str1))


				# time.sleep(1)
				# ser.flushInput()
			# data2= str(binascii.b2a_hex(ser.read(240)))
			# print(data2)
			# time.sleep(1)


		# n=ser.in_waiting()
		# if n: 
		# # while(1):
		# 	data2= str(binascii.b2a_hex(ser.read(24)))
		# 	print(data2)
		# 	# time.sleep(2)
		
		ser.close()

	except Exception as e:
		print("Exception: ",e)

