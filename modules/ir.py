import RPi.GPIO as GPIO
import subprocess

GPIO.setmode(GPIO.BCM)
pin = 7
GPIO.setup(pin, GPIO.IN)
Debug = False

def getpowerstatus(initpolls = 10000, checks = 100):
	power_value = 0
	for l in range(checks):
		polls = initpolls
		for l in range(initpolls):
			if GPIO.input(pin) == GPIO.LOW:
				polls = polls - 1
		if polls < initpolls:
			power_value = power_value + 1
			if Debug == True:
				print power_value
		else:
			power_value = power_value - 1
			if Debug == True:
				print power_value
	if power_value < 0:
		return 0
	elif power_value > 0:
		return 1
	else:
		return "Error Reading Sonic Sensor"

def irsend(device, button):
	subprocess.call("irsend SEND_ONCE %s %s" % (device, button), shell=True)
	return None

def aircon(command_name, command_value):
	if command_name == "power":
		power = "POWER COMMAND PASSED NO ISSUE"
		if command_value == "toggle":
			irsend("aircon","KEY_POWER")
		elif command_value == "2":
			if getpowerstatus() == 0:
				irsend("aircon","KEY_POWER")
			if getpowerstatus() == 1:
				irsend("aircon","KEY_POWER")
				irsend("aircon","KEY_POWER")
		elif command_value == "1":
			if getpowerstatus() == 0:
				irsend("aircon","KEY_POWER")
			else:
				power = power + " (AC unit was already on. No IR trigger sent.)"
		elif command_value == "0":
			if getpowerstatus() == 1:
				irsend("aircon","KEY_POWER")
			else:
				power = power + " (AC unit was already off. No IR trigger sent.)"
		elif command_value == "status":
			powerstatus = getpowerstatus()
			if powerstatus == 1:
				powerstatus = "ON"
			elif powerstatus == 0:
				powerstatus = "OFF"
			else:
				powerstatus = "Error Reading Power Status"
			power = "The Air Conditioner is Currently %s" % powerstatus
		else:
			power = 'INVALID VARIABLE GIVEN (%s).  Please use: "toggle", "1", "0", "status."' % power
	if command_name == "mode":
	    mode = int(command_value)
	    for _ in range(mode):
	        irsend("aircon","KEY_MODE")
	if command_name == "fan":
	    fan = int(command_value)
	    for _ in range(fan):
	        irsend("aircon","KEY_F")
	if command_name == "temp":
	    temp = int(command_value)
	    if temp < 0:
	        for _ in range(abs(temp) + 1):
	            irsend("aircon","KEY_DOWN")
	    if temp > 0:
	        for _ in range(temp + 1):
	            irsend("aircon","KEY_UP")
	if command_name == "abstemp":
	    for _ in range(16):
	        irsend("aircon","KEY_DOWN")
	    for _ in range(int(command_value) - 64):
	        irsend("aircon","KEY_UP")      
	return "successfully ran AirCon function"     

def run(input_value):
	input_value = input_value.split('$')
	device = input_value[0]
	print device
	if not input_value[1].count('!') == 0:
		commands = input_value[1].split('!')
	else:
		commands = [input_value[1]]
	print("ir commands: " + str(commands))
	for command_raw in commands:
		try:
			command_raw = command_raw.split('|')
			command_name = command_raw[0]
			command_value = command_raw[1]
			print("trying command :" + str(command_name) + " with: " + str(command_value))
			if device == "aircon":
				aircon(command_name, command_value)
			else:
				irsend(command_name, command_value)
		except:
			print("Error Running Command")






if __name__ == "__main__":
	Debug = True
	print run("aircon$power|2")
