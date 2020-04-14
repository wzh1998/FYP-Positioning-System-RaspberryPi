# FYP-Positioning-System-RaspberryPi
## Prerequisite
>     sudo pip3 install pymysql
      sudo pip3 install pyserial

## Usage
> python3 main.py

## File
+ main.py: the multi-thread program to read card and upload to the database.
+ card_info.txt: store epc code of each card.
+ equipment_info.txt: store code of each equipment.
+ data.csv: a dataset used to predict location based on RSSI reading.