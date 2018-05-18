import time
import sys
import server_parser
import imp


#Address of Handling Sever
server_address = "home.lukeschimmel.com:2301"
#iot_id of the device
iot_id = "4"
#delete requests from Handling Server once read?
delete = True
#sets the pinging service to run
run = True
#Sets delay (in seconds) between pings
ping_timer = 5


run_count = 0
while run == True:
	run_count = run_count + 1
	print(run_count)

	checkupdate = server_parser.checkupdate(iot_id, server_address, delete)
	if not checkupdate == None:
		print(checkupdate)
		commands = server_parser.parse_server(checkupdate)
		print(commands)
		for command in commands:
			print("command: " + command)
			service = command[0:2]
			print("service: " + service)
			values = command[2:]
			print ("values: " + values)
			try:
				print(imp.load_source("{}.py".format(service),"modules/{}.py".format(service)).run(values))
			except:
				print "Error in running command:", sys.exc_info()
	time.sleep(ping_timer)