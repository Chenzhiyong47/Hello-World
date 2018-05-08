
files:

├── background.py
	running in the background all the time.
	to control the motor and record the distance ultrasound measuring.
	
├── config.py
	the config file of program

├── database.py
	operate database named "time-distance"
	including: add, delete, find, modify and etc.

├── hardware.py
	to control ultrasound and motor

├── INIT.py
	initialize database. (create tables, and add the initialized data.)


run:
	
	python3 background.py

	if initialize the database:
	
		python3 INIT.py


