import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)


def GPIO_Control(pin, command, delay):
	pin = int(pin)
	GPIO.setup(pin,GPIO.OUT)
	if delay:
		GPIO.output(pin, True)
		time.sleep(float(delay))
		GPIO.output(pin, False)
	else:
		command = int(command)
		GPIO.output(pin, command)
	return



def run(commands):
	if not commands.count("!") == 0:
		commands = commands.split("!")
	else:
		commands = [commands]
	for command_raw in commands:
		command_raw = command_raw.split('|')
		GPIO_pin = command_raw[0]
		command = command_raw[1]
		if GPIO_pin	== "7":
			return "error: this Pin is already in use by the Sonic Sensor"
		if not (command == "1" or command == "0" or command[0:6] == "toggle" or command[0:6] == "Toggle"):
			return "error: you can only command 1, 0, or toggle"
		else:
			delay = None
			if command[0:6] == "toggle" or command[0:6] == "Toggle":
				delay = 1
				if command[6:]:
					delay = command[6:]
					command = "toggle"
			print delay
			print command
			print GPIO_pin
			GPIO_Control(GPIO_pin, command, delay)



if __name__ == '__main__':
	print run("19|toggle1!26|toggle0.1")



