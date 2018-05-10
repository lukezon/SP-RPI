import subprocess



def run(commands):
	commands = commands.replace('|','.')
	if not commands.count("!") == 0:
		commands = commands.split("!")
	else:
		commands = [commands]
	for command in commands:
		result = subprocess.call("cm-scripts/%s" % command)
	return result