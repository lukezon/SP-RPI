import time
import server_parser
import infrared as ir

#Address of Handling Sever
server_address = "10.0.1.90:8080"
#iot_id of the device
iot_id = "4"
#delete requests from Handling Server once read?
delete = True
#sets the pinging service to run
run = True


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
				service.run(values)
			except:
				print("Error in running command")
	time.sleep(2)