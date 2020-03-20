import pymysql
import time

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
		print("Warning: Update failed at ..., please check the network connection.")
		db.rollback()

	# Close SQL connection
	db.close()

	return

if __name__ == '__main__':
	SQL_Equipment_Update("EQ0001", "Floor 5, Room 502")

